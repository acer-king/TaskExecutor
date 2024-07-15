from fastapi import HTTPException
import aiodocker
from app import util
from app.schemas import Resources


class DockerManager:
    def __init__(self):
        self.client = aiodocker.Docker()
        self.volume_name = util.get_random_hash_str()

    async def docker_volume_create(self, storage_size):
        try:
            await self.client.volumes.create({
                'Name': self.volume_name,
                'Driver': 'local',
                'DriverOpts': {
                    'type': 'tmpfs',
                    'device': 'tmpfs',
                    'o': f'size={storage_size}'
                }
            })
        except aiodocker.exceptions.DockerError as e:
            raise HTTPException(status_code=400, detail=f"Error creating volume: {e}")

    async def volume_delete(self):
        await util.run_subprocess(f"docker volume rm {self.volume_name}")

    def handle_volume(func):
        """
        decorator that handle volume of docker container.
        create the volume before creating the container and delete the volume after execution of
        container
        :return:
        """

        async def wrapper(self, code: str, resources: Resources):
            await self.docker_volume_create(resources.storage[:-1])
            result = await func(self, code, resources)
            await self.volume_delete()
            return result

        return wrapper

    @handle_volume
    async def run_container(self, code: str, resources: Resources) -> str:
        """
        execution python code inside docker container using resources.
        :param code: python code
        :param resources: python resources
        :return:
        """
        config = {
            'Image': 'python:3.9-slim',
            'Cmd': ['python', '-c', code],
            'HostConfig': {
                'NanoCPUs': int(resources.cpu) * 1000000000,
                'Memory': util.convert_memory(resources.ram),
                'DeviceRequests': [
                    {
                        'Driver': 'nvidia',
                        'Count': int(resources.gpu),
                        'Capabilities': [['gpu']]
                    }
                ] if int(resources.gpu) > 0 else [],
                'Binds': [
                    f'{self.volume_name}:/mnt/volume'
                ]
            }
        }

        container_name = util.get_random_hash_str()
        container = await self.client.containers.create_or_replace(
            name=str(container_name).lower(), config=config
        )

        await container.start()
        await container.wait()

        logs = await container.log(stdout=True, stderr=True)

        await container.stop()
        await container.delete()
        return ''.join(logs)

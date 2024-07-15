from fastapi import HTTPException
import aiodocker
from app import util
from app.schemas import Resources


class DockerManager:
    def __init__(self):
        self.client = aiodocker.Docker()
        self.volume_name = "test"

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
                ] if int(resources.gpu) > 0 else []
            }
        }

        container_name = "test"
        container = await self.client.containers.create_or_replace(
            name=str(container_name), config=config
        )

        await container.start()


        logs = await container.log(stdout=True, stderr=True)

        await container.stop()
        await container.delete()
        return ''.join(logs)

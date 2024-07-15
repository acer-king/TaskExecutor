import hashlib
import datetime
import asyncio
import logging


def get_random_hash_str():
    hashlib.sha1().update(str(datetime.datetime.now()).encode("utf-8"))
    return hashlib.sha1().hexdigest()[:10]


def convert_memory(ram: str) -> int:
    units = {'MB': 1e6, 'GB': 1e9}
    return int(float(ram[:-2]) * units[ram[-2:]])


async def run_subprocess(cmd):
    # Start a subprocess
    process = await asyncio.create_subprocess_shell(
        cmd=cmd,  # Replace this with your command and arguments
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Read stdout and stderr
    stdout, stderr = await process.communicate()

    # Print the output
    logging.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logging.info(f"[stderr]\n{stderr.decode()}")


async def run_sudo_subprocess(command, sudo_password):
    process = await asyncio.create_subprocess_exec(
        'sudo', '-S', *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Write the sudo password to stdin and close it
    stdout, stderr = await process.communicate(input=(sudo_password + '\n').encode())

    # Print the output
    logging.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logging.info(f"[stderr]\n{stderr.decode()}")

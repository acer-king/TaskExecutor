# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings:
    default_cpus: str = os.getenv("DEFAULT_CPUS")
    default_gpus: str = os.getenv("DEFAULT_GPUS")
    default_ram: str = os.getenv("DEFAULT_RAM")
    default_storage: str = os.getenv("DEFAULT_STORAGE")
    default_time_out: int = int(os.getenv("TIME_OUT"))
    default_docker_img: str = os.getenv("DOCKER_IMG")

    class Config:
        env_file = ".env"


settings = Settings()

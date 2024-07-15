# Task Manager API

This project is a Python API using FastAPI, designed to interact with client-side requests for managing and executing tasks within Docker containers.
This project can be used to build services that provides computing resources such as cpu, gpu, ram, storage like AWS.
## Getting Started

### Prerequisites

- Docker
- Python 3.9+

### Installation and Runing Application

1. Clone the repository:
   ```bash
   git clone https://github.com/acer-king/TaskExecutor
   cd TaskExecutor
2. Install required python pkgs:
   ```bash
   pip install -r requirements.txt
3. Run fastapi applicatoin:
   ```bash
   uvicorn app.main:app --reload

### Project description

- In first step, based on request_body, first create volume with storage.
- In second, create docker container with given resources such as cpu, gpu, ram.
- In third, stop the docker container and collects logs using stdin, stdout to return result.
- In fourth, delete the volume created before and return result


### Challenges

- aiodocker volume delete function was not working somehow, so I used async subprocess to delete the docker volume using command line.
- aiodocker doesn't pull image from internet. so I solved this problem by calling subprocess on startup application to download python docker image to local.
- for validation of input request, i used regex and pydantic.
- I used dependency injection for using services.


### [![Watch the video](https://drive.google.com/file/d/18VtdL37s4EroQxxpmdprH0LmiJ189PyE/view?usp=sharing)
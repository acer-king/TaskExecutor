# Task Manager API

This project is a Python API using FastAPI, designed to interact with client-side requests for managing and executing tasks within Docker containers.
This project can be used to build services that provides computing resources such as cpu, gpu, ram, storage like AWS.
## Getting Started

### Prerequisites

- Docker
- Python 3.9+

### Installation

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

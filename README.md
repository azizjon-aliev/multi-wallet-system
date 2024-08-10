# Multi Wallet System

## Setup
### Clone the repository:
```bash
git clone https://github.com/azizjon-aliev/multi-wallet-system.git
```
### Cd into the project directory:
```bash
cd multi-wallet-system
```

### Create and configure environment variables:
```bash
cp .env.example .env
```

## Build and run the Docker containers
```bash
docker-compose up -d --build
```

## Running without Docker
### Create and activate a virtual environment:
```bash
python3 -m venv venv &&

source venv/bin/activate
```
### Install the dependencies:
```bash
pip install -r requirements.txt
```

### Run the project:
```bash
python -m main
```


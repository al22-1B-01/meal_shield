# Meal Shield

## How to operate docker
### setup
1. Install with : `git clone https://github.com/al22-1B-01/meal_shield.git`
### docker configuration
1. `docker compose up -d --build`
### Connect to and disconnect from docker
1. connect : `docker compose exec <frontend or backend> bash`
2. disconect : `exit`
### Starting and Stopping Containers
1. Starting : `docker stop <container name>`
2. Stopping : `docker start <container name>`

## Directory structure
```text
./
├── .dockerignore
├── .git
├── .gitattributes
├── .github
├── .gitignore
├── Makefile
├── README.md
├── backend
├── compose.yaml
├── env.sample
└── frontend
```

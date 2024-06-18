# Meal Shield

## How to operate docker
### setup
1. Install with : `git clone https://github.com/al22-1B-01/meal_shield.git`
### setup API key
1. Get API key：Access `https://platform.openai.com/settings/profile?tab=api-keys`
   - Reference：https://nicecamera.kidsplates.jp/help/6648/
2. copy env file：`cp backend/env.sample backend/.env`
3. write to API key: `backend/.env`
### docker configuration
1. `docker compose up -d --build`
### Connect to and disconnect from docker
1. connect : `docker compose exec <frontend or backend> bash`
2. disconect : `exit`
### Starting and Stopping Containers
1. Starting : `docker compose start`
2. Stopping : `docker compose stop`

## Coding
### Directory structure
- frontend App to `frontend`
- backend App to `frontend`
### Test
1. must clear this command on docker
2. must clear tests on GitHub actions

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
├── docs
├── env.sample
└── frontend
```

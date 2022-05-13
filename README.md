# git-to-know-me

## Setup

Install dependencies
```bash
pip3 install -r requirements.txt
```

## Run

To run you need proper `.env` file with secret tokens

Monolith version:
```bash
uvicorn gtkm.main:app --reload --env-file .env
```

Microservice version:
- Install nginx (https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
- Windows:
-- Place the unzipped nginx files in folder "nginx" in the main folder of the project
-- Swap the file "nginx/conf/nginx.conf" for the one provided with the project
-- Open cmd in the "nginx" folder
-- to start nginx: `start nginx`
- Linux:
-- nginx files are located in /usr/bin/nginx
-- to start nginx: `/usr/bin/nginx -c <path_to_conf_file>`
- additional nginx commands:
-- `nginx -s reload`
-- `nginx -s quit`
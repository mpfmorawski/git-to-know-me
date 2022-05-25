# git-to-know-me

## Setup

Install dependencies

```bash
pip3 install -r requirements.txt
```

## Docker installation

Based ond: https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu
1. Install Docker using the following command:
```bash
sudo apt install docker.io
```
2. Install all the dependency packages using the following command:
```bash
sudo snap install docker
```

## Docker-compose installation

Based on: https://phoenixnap.com/kb/install-docker-compose-on-ubuntu-20-04
1. Upgrade and Update:
```bash
sudo apt update
sudo apt upgrade
```
2. Install curl:
```bash
sudo apt install curl
```
3. Download the Latest Docker-compose Version
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker
-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
4. Change File Permission:
```bash
sudo chmod +x /usr/local/bin/docker-compose
```
5. Check Docker Compose Version:
```bash
sudo docker–compose --version
```

### Minikube installation

Based on: https://minikube.sigs.k8s.io/docs/start/
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Run

To run you need proper `.env` file with secret tokens

### Monolith version

```
uvicorn gtkm.main:app --reload --env-file .env
```

### Monolith version - Docker

```bash
docker-compose build
docker-compose up
```

### Microservice version

- Install nginx (https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
- Windows:
  - Place the unzipped nginx files in folder "nginx" in the main folder of the project
  - Swap the file "nginx/conf/nginx.conf" for the one provided with the project
  - Open cmd in the "nginx" folder
  - to start nginx: `start nginx`
- Linux:
  - Open terminal in the "nginx" folder
  - to start nginx: `sudo nginx -p ./ -c conf/nginx.conf`
- additional nginx commands:
  - `nginx -s reload`
  - `nginx -s quit`
- Run `main_microservices.py`
- 

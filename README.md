# git-to-know-me

## Setup

Install dependencies

```bash
pip3 install -r requirements.txt
```

## Run

```bash
source .env #env file with secret tokens
uvicorn gtkm.main:app --reload
```

# git-to-know-me

## Setup

Install dependencies

```bash
pip3 install -r requirements.txt
```

## Run

To run you need proper `.env` file with secret tokens

```bash
uvicorn gtkm.main:app --reload --env-file .env
```

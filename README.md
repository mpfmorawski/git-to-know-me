# git-to-know-me

## Setup

Install dependencies

```bash
pip3 install -r requirements.txt
```

## Run

```bash
python -c "from dotenv import load_dotenv; import uvicorn; load_dotenv(); uvicorn.run('gtkm.main:app', reload=True)"
```

# mini-recsys
mini recommender system with FastAPI (WIP)

## Environments
- Python 3.9.4

```bash
pip3 install -r requirements.txt
```

## Run

```bash
export PYTHONPATH=src/.
gunicorn src.app.main:app -b 0.0.0.0:5000 -k "uvicorn.workers.UvicornWorker" --timeout=20
```

## URL
- http://localhost:5000/
- http://localhost:5000/docs

## TODO
- [x] execute app with gunicorn
- [ ] execute app on docker container
- [x] make up front side 
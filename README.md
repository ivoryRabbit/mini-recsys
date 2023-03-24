# mini-recsys
mini recommender system with FastAPI

## Environments
- Python 3.9.4

## Run
### Local
```bash
pip3 install -r requirements.txt

export PYTHONPATH=src/.
scripts/run-app.sh
```

### Docker container
```bash
docker build -t mini-recsys -f docker/Dockerfile .
docker run -it mini-recsys -p 5000:5000
```

## URL
- http://localhost:5000/
- http://localhost:5000/docs

## TODO
- [x] execute app with gunicorn
- [x] execute app on docker container
- [ ] make up front side 
# mini-recsys
mini recommender system with FastAPI

## Environments
- Python 3.9.4

## Run
### Local
```bash
pip3 install -r backend/requirements.txt \
  && cd backend/src \
  && gunicorn main:app -b :8080 -k uvicorn.workers.UvicornWorker -t 60
```

### Docker container
```bash
docker build -t mini-recsys -f backend/Dockerfile . \
  && docker run -it mini-recsys -p 8080:8080
```

## URL
- http://localhost:8080/
- http://localhost:8080/docs

## TODO
- [x] execute app with gunicorn
- [x] execute app on docker container
- [ ] porting web application using streamlit 
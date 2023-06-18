# mini-recsys
mini recommender system with FastAPI and Streamlit

## Environments
- Python 3.9.4

## Run
### Local
```shell
# launch FastAPI application server
pip3 install -r backend/requirements.txt \
  && cd backend/src \
  && gunicorn main:app -b :8080 -k uvicorn.workers.UvicornWorker
```
```shell
# launch Streamlit application server
pip3 install -r frontend/requirements.txt \
  && cd frontend/src \
  && streamlit run main.py
```

### Docker container
```shell
docker-compose up --build
```

## URL
- [UI](http://localhost:8501)
- [Docs](http://localhost:8080/docs)

## TODO
- [x] execute app with gunicorn
- [x] execute app on docker container
- [x] porting web application using streamlit 
- [ ] improve streamlit UI for recommendation result 
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
  && uvicorn main:app --port 8080 --reload
```
```shell
# launch Streamlit application server
pip3 install -r frontend/requirements.txt \
  && cd frontend/src \
  && streamlit run main.py --server.port 8501
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
- [ ] test and fix bugs
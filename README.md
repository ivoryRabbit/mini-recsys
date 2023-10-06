# mini-recsys
mini recommender system with FastAPI and Streamlit

## Environments
- Python 3.9.4
- Docker

---
## Run
### Local
```shell
# launch FastAPI application server
pip3 install -r server/requirements.txt \
  && cd server/src \
  && uvicorn main:app --port 8080 --reload
```
```shell
# launch Streamlit application server
pip3 install -r client/requirements.txt \
  && cd client/src \
  && streamlit run main.py --server.port 8501
```

### Docker container
```shell
docker-compose up --build
```
---
## URL
### UI
- [http://localhost:8501](http://localhost:8501)

![Demo UI](https://github.com/ivoryRabbit/mini-recsys/assets/30110145/a3e6c4a8-4bc6-46c2-a107-3c04221acbd5)

### Docs
- [http://localhost:8080/docs](http://localhost:8080/docs)

---
## TODO
- [x] execute app with gunicorn
- [x] execute app on docker container
- [x] porting web application using streamlit 
- [x] improve streamlit UI for recommendation result
- [x] test and fix bugs
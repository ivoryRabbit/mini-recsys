FROM python:3.9.4

WORKDIR /opt/server/

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8080

ENTRYPOINT ["gunicorn", "main:app", "-b", ":8080", "-k", "uvicorn.workers.UvicornWorker"]
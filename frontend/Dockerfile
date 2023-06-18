FROM python:3.9.6-slim

WORKDIR /opt/frontend/

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# /opt/frontend/main.py
COPY src .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port", "8501"]
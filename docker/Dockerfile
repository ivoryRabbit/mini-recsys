FROM python:3.9.4

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

ENV APP_PATH="/opt/app"
ENV SOURCE_PATH="$APP_PATH/src"
ENV PYTHONPATH="$SOURCE_PATH:$PYTHONPATH"

WORKDIR $APP_PATH

COPY src $SOURCE_PATH

COPY scripts/run-app.sh /run-app.sh

RUN chmod +x /run-app.sh

EXPOSE 5000

ENTRYPOINT ["/run-app.sh"]

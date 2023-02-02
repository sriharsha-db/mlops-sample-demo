FROM python:3.9.16-slim-bullseye

COPY app app
COPY models models
COPY service-requirements.txt /

RUN apt-get update && apt-get -y install gcc g++ \
    && pip install --no-cache-dir --upgrade -r models/requirements.txt \
    && pip install --no-cache-dir -r service-requirements.txt

EXPOSE 8080
CMD ["uvicorn","app.webservice:app","--host","0.0.0.0","--port","8080"]
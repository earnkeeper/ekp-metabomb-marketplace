FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./server.py ./server.py
COPY ./features ./features
COPY ./sdk ./sdk
COPY ./static ./static

CMD [ "python3", "server.py" ]
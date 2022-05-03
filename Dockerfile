FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY ./features ./features
COPY ./sdk ./sdk
COPY ./static ./static
COPY ./util ./util
COPY ./server.py ./server.py

CMD [ "python3", "server.py" ]
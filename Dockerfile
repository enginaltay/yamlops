FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apk update
RUN apk add curl

COPY . /usr/src/app

EXPOSE 5000
EXPOSE 80

CMD [ "python", "./app_with_mongo.py" ]

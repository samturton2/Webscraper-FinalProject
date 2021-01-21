FROM python:3.8 AS app

WORKDIR /usr/src/flaskapp

COPY . .

RUN pip install -r requirements.txt

# second stage build

FROM python:3.8-slim
COPY --from=app /usr/src/flaskapp /usr/src/flaskapp

ENV AWS_SECRET_KEY=$AWS_SECRET_KEY
ENV AWS_ACCESS_KEY=$AWS_ACCESS_KEY

WORKDIR /usr/src/flaskapp

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]

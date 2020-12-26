FROM python:3.8-alpine

WORKDIR /opt/build
COPY Pipfile* ./

RUN apk add build-base libffi-dev openssl-dev python3-dev bash npm curl && \
    pip install pipenv && \
    npm install -g serverless@2.16.1 && npm install -g serverless-offline && \
    pipenv --python 3.8 && pipenv sync && pipenv sync --dev && \
    rm /var/cache/apk/*
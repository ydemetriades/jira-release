FROM python:3.6.4-alpine3.7
LABEL maintainer="yiannis.demetriades@gmail.com"

ENV LANG C.UTF-8

RUN apk update && \
    apk upgrade && \
    pip install --no-cache-dir requests

COPY script/jira-release.py /jira-release.py

ENTRYPOINT ["python", "/jira-release.py"]
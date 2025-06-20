FROM python:alpine
LABEL maintainer="yiannis.demetriades@gmail.com"

ENV LANG=C.UTF-8

RUN apk update && \
    apk upgrade && \
    pip install --no-cache-dir requests argparse

COPY script/jira-release.py /jira-release.py

ENTRYPOINT ["python", "/jira-release.py"]
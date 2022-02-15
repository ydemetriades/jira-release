# Jira Release

## Description:

Easily create Jira releases from the comfort zone of your CLI! :)

`ydemetriades/jira-release` docker image enables the creation of Release Versions in Jira.
You can find it at [DockerHub](https://hub.docker.com/repository/docker/ydemetriades/ydemetriades/jira-release).

## Runtime & Tags

`ydemetriades/jira-release` is available both for Linux and Windows.

### Linux

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0__|__v1.0__|`ydemetriades/jira-release:v1.0`|
|__v2.0__|__v2.0__|`ydemetriades/jira-release:v2.0`|

_Note_: `latest` tag points to `v2.0`

### Windows

`ydemetriades/jira-release` on Windows is available only for `1809`

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0-win1809__|__v1.0__|`ydemetriades/jira-release:v1.0-win1809`|
|__v2.0-win1809__|__v2.0__|`ydemetriades/jira-release:v2.0-win1809`|

Note: `latest-win1809` tag points to `v2.0-win1809`

## Parameters

From `v2.0.0` all parameters are passed as executable arguments or by environment variables.

|Parameter|Environment Variable|Required|Description|Default Value|Available Options|Example|
|:--:|:------:|:------:|-----------|:-------------:|:-----------------:|-------|
|`--version`, `-v`|`JIRA_VERSION_NAME`|Yes|The unique name of the version|-|-|-v v1.0|
|`--project`, `-p`|`JIRA_PROJ`|Yes|The ID of the project to which this version is attached|-|-|-p 10000|
|`--user`, `-u`|`JIRA_AUTH_USER`|Yes|The Jira authentication user [email]|-|-|-u user|
|`--password`|`JIRA_AUTH_PASSWORD`|Yes|Jira API Authorization Password / API Token|-|-|--password 12345|
|`--description`, `-d`|`JIRA_VERSION_DESCRIPTION`|No|The description of the version. Default value is an empty string.|-|-|-d "My awesome version description!"|
|`--update`|`JIRA_VERSION_UPDATE`|No|Indicates whether to update/create the version. Avoidance/`False` indicates creation where definition/`True` indicated update|-|-|-|
|`--released`|`JIRA_VERSION_RELEASED`|No|Indicates that the version is released.|-|-|--released|
|`--archived`|`JIRA_VERSION_ARCHIVED`|No|Indicates that the version is archived.|-|-|--archived|
|`--url`|`JIRA_URL`|No|Jira Url|https://jira.org|-|--url https://jira.mydomain.com|
|`--api-version`|`JIRA_API_VERSION`|No|Jira API Version|__3__|[2, 3]|--api-version 3|

## Notes

1. Enable Jira Api from Administration Settings

2. User __JIRA_AUTH_USER__ must be an Administrator for __JIRA_PROJ__ project

## Examples

### CLI Examples

```bash
jira-release.py -v v1.0.0 -p 10000 -u youremail@example.com --password 'YOUR_API_TOKEN'
```

### Docker Examples

```
docker run -d --rm \ 
-e JIRA_VERSION_NAME=v1.0 \
-e JIRA_PROJ=TES \
-e JIRA_AUTH_USER=user \
-e JIRA_AUTH_PASSWORD=password \
ydemetriades/jira-release
```

```
docker run -d --rm \ 
-e JIRA_VERSION_NAME=v1.0 \
-e JIRA_PROJ=TES \
-e JIRA_AUTH_USER=user \
-e JIRA_AUTH_PASSWORD=password \
-e JIRA_URL=http://jira.mydomain.com \
-e JIRA_VERSION_RELEASED=false \
-e JIRA_VERSION_DESCRIPTION=Fixed issue TES-101 \
ydemetriades/jira-release
```

## Maintainers


[Yiannis Demetriades](https://github.com/ydemetriades)

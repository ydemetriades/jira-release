# Jira Release

## Description:

`ydemetriades/jira-release` docker image enables the creation of Release Versions in Jira.
You can find it at [DockerHub](https://hub.docker.com/repository/docker/ydemetriades/ydemetriades/jira-release).

## Runtime & Tags

`ydemetriades/jira-release` is available both for Linux and Windows.

### Linux

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0__|__v1.0__|`ydemetriades/jira-release:v1.0`|

_Note_: `latest` tag points to `v1.0`

### Windows

`ydemetriades/jira-release` on Windows is available only for `1903`

|Tag|Version|Pull|
|:-:|:-----:|----|
|__v1.0-win1903__|__v1.0__|`ydemetriades/jira-release:v1.0-win`|

Note: `latest-win` tag points to `v1.0-win`

## Parameters

Parameters are defined as environment variables

|Name|Required|Description|Default Value|Available Options|Example|
|:--:|:------:|-----------|-------------|-----------------|-------|
|__JIRA_VERSION_NAME__|Yes|Release Name|-|-|v1.0|
|__JIRA_PROJ__|Yes|Jira Project Short Name|-|-|TES|
|__JIRA_AUTH_USER__|Yes|Jira API Authorization Username|-|-|user|
|__JIRA_AUTH_PASSWORD__|Yes|Jira API Authorization Password|-|-|password|
|__JIRA_URL__|No|Jira Url|https://jira.org|-|http://jira.mydomain.com|
|__JIRA_VERSION_RELEASED__|No|Indicates whether the current version has been released|`true`|`true`, `false`|`false`|
|__JIRA_VERSION_DESCRIPTION__|No|Description for the current version|Version {JIRA_VERSION_NAME}|-|Fixed issue TES-101|

## Notes

1. Enable Jira Api from Administration Settings

2. User __JIRA_AUTH_USER__ must be an Administrator for __JIRA_PROJ__ project

## Examples

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

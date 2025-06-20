# Jira Release

## Description

Easily create Jira releases from the comfort of your CLI! :)

`ydemetriades/jira-release` is a Docker image that enables the creation of Release Versions in Jira.
You can find it at [DockerHub](https://hub.docker.com/r/ydemetriades/jira-release).

## Prerequisites

- Enable the Jira API from Administration Settings.
- The user specified by `JIRA_AUTH_USER` must be an Administrator for the `JIRA_PROJ` project.

## Runtime & Tags

`ydemetriades/jira-release` is available for both Linux and Windows.

### Linux

| Tag | Pull |
|:-:|----|
| **v3.2** | `ydemetriades/jira-release:v3.2` |
| **v3.1** | `ydemetriades/jira-release:v3.1` |
| **v3.0** | `ydemetriades/jira-release:v3.0` |
| **v2.0** | `ydemetriades/jira-release:v2.0` |
| **v1.0** | `ydemetriades/jira-release:v1.0` |

_Note_: The `latest` tag points to `v3.2`.

## Parameters

From `v2.0.0`, all parameters are passed as executable arguments or by environment variables.

| Parameter | Environment Variable | Required | Description | Default Value | Available Options | Example |
|:--:|:------:|:------:|-----------|:-------------:|:-----------------:|-------|
| `--version`, `-v` | `JIRA_VERSION_NAME` | Yes | The unique name of the version | - | - | -v v1.0 |
| `--project`, `-p` | `JIRA_PROJ` | Yes | The ID of the project to which this version is attached | - | - | -p 1000 |
| `--user`, `-u` | `JIRA_AUTH_USER` | Yes | The Jira authentication user (email address) | - | - | -u user@example.com |
| `--password` | `JIRA_AUTH_PASSWORD` | Yes | Jira API Authorization Password or API Token | - | - | --password 12345 |
| `--description`, `-d` | `JIRA_VERSION_DESCRIPTION` | No | The description of the version. Default value is an empty string. | - | - | -d "My awesome version description!" |
| `--update` | `JIRA_VERSION_UPDATE` | No | Indicates whether to update or create the version. If omitted or set to `False`, a new version is created. If set to `True`, the version is updated. | - | - | - |
| `--released` | `JIRA_VERSION_RELEASED` | No | Indicates that the version is released. | - | - | --released |
| `--archived` | `JIRA_VERSION_ARCHIVED` | No | Indicates that the version is archived. | - | - | --archived |
| `--url` | `JIRA_URL` | No | Jira URL | https://jira.org | - | --url https://jira.mydomain.com |
| `--api-version` | `JIRA_API_VERSION` | No | Jira API Version | **3** | [2, 3] | --api-version 3 |

## Notes

1. Enable Jira Api from Administration Settings

2. User __JIRA_AUTH_USER__ must be an Administrator for __JIRA_PROJ__ project

## Examples

### CLI Example

If you are running the script directly (e.g., in a Python environment):

```bash
python script/jira-release.py -v v1.0.0 -p 10000 -u youremail@example.com --password 'YOUR_API_TOKEN'
```

### Docker Examples

```bash
docker run -d --rm \
  -e JIRA_VERSION_NAME=v1.0 \
  -e JIRA_PROJ=TES \
  -e JIRA_AUTH_USER=user \
  -e JIRA_AUTH_PASSWORD=password \
  ydemetriades/jira-release
```

```bash
docker run -d --rm \
  -e JIRA_VERSION_NAME=v1.0 \
  -e JIRA_PROJ=1000 \
  -e JIRA_AUTH_USER=user \
  -e JIRA_AUTH_PASSWORD=password \
  -e JIRA_URL=https://jira.mydomain.com \
  -e JIRA_VERSION_RELEASED=false \
  -e JIRA_VERSION_DESCRIPTION="Fixed issue TES-101" \
  ydemetriades/jira-release
```

## Maintainers

[Yiannis Demetriades](https://github.com/ydemetriades)

## License

See [LICENSE](./LICENSE) for details.

## Jira Authentication and Authorization

To interact with the Jira API, you need to authenticate using an API Token or a Scoped API Token. These tokens are used in place of your password for increased security and are required for all API operations.

### API Token
- An API Token is a secure way to authenticate with Jira Cloud REST APIs.
- You can generate and manage your API tokens from your Atlassian account: [Manage API tokens for your Atlassian account](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- Use the generated token as the value for the `JIRA_AUTH_PASSWORD` environment variable or the `--password` argument.

### Scoped API Token
- Scoped API Tokens provide more granular access control, allowing you to limit the permissions granted to the token.
- For most use cases, a standard API Token is sufficient, but if you require more control, consider using a Scoped API Token (if available for your Jira instance).
- The minimum required scopes for this tool are:
  - `read:project-version:jira` (granular): View project versions.
  - `write:project-version:jira` (granular): Create and update project versions.
- Refer to Atlassian documentation for details on creating and using Scoped API Tokens.

**Note:**
- Never share your API tokens publicly or commit them to version control.
- If you suspect your token has been compromised, revoke it immediately from your Atlassian account settings.

## How to Retrieve the Jira Project ID

To find the Project ID required for the `JIRA_PROJ` parameter, you can use your web browser and the Jira REST API:

1. **Using the REST API:**
   - Open your browser and go to:
     
     ```
     <JIRA_BASE_URL>/rest/api/latest/project/<project_key>
     ```
     
     Replace `<JIRA_BASE_URL>` with your Jira instance URL (e.g., `https://yourcompany.atlassian.net`) and `<project_key>` with your project's key (e.g., `TES`).
   - The resulting JSON will include a field like:
     
     ```json
     {
       ...
       "id": "10000",
       "key": "TES",
       ...
     }
     ```
   - The value of `id` is your Project ID (e.g., `10000`).

2. **Tip:**
   - You can paste the JSON output into a JSON beautifier for easier reading.

For more details, see the [Atlassian support article](https://support.atlassian.com/jira/kb/how-to-get-the-id-of-a-jira-project-from-a-web-browser/).

## Jira API Documentation

For advanced usage and integration, refer to the official Jira REST API documentation for managing project versions:

- **API Reference:** [Jira REST API v3 - Project Versions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/#api-rest-api-3-version-post)

### Creating a Version (POST /rest/api/3/version)

To create a new version in a Jira project, send a POST request to:

```
POST /rest/api/3/version
```

**Request Body Example:**
```json
{
  "name": "New Version 1",
  "description": "An excellent version",
  "projectId": 10000,
  "released": true,
  "releaseDate": "2010-07-06"
}
```

**Required Permissions:**
- Administer Jira (global) or Administer Projects (project)
- OAuth 2.0 scope: 
    The minimum required scopes for this tool are:
    - `read:project-version:jira` (granular): View project versions.
    - `write:project-version:jira` (granular): Create and update project versions.

For more details, see the [API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/#api-rest-api-3-version-post).

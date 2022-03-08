#!/usr/bin/env python
from ast import parse
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json
from requests.exceptions import HTTPError

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=False, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser( description='Create Jira versions easily', epilog="And that's how we create Jira versions easily!")

### Required Arguments
parser.add_argument('--version', '-v', action=EnvDefault, envvar='JIRA_VERSION_NAME', type=str, required=True, help='The unique name of the version. Can be specified by environment variable JIRA_VERSION_NAME.')
parser.add_argument('--project', '-p', action=EnvDefault, envvar='JIRA_PROJ', type=int, required=True, help='The ID of the project to which this version is attached.')
parser.add_argument('--user', '-u', action=EnvDefault, envvar='JIRA_AUTH_USER', type=str, required=True, help='The Jira authentication user email.')
parser.add_argument('--password', action=EnvDefault, envvar='JIRA_AUTH_PASSWORD', type=str, required=True, help='Jira API Authorization Password / API Token.')

### Optional Arguments
parser.add_argument('--description', '-d', action=EnvDefault, envvar='JIRA_VERSION_DESCRIPTION', default=None, type=str, help='The description of the version. Default value is an empty string.')

# Should update instead of create
parser.add_argument('--update', action=EnvDefault, envvar='JIRA_VERSION_UPDATE', type=bool, default=False, help='Indicates whether to update or create the version. Can be specified by environment variable JIRA_VERSION_UPDATE. Default value is false.')

parser.add_argument('--new-version', action=EnvDefault, envvar='JIRA_NEW_VERSION_NAME', type=str, help='The new name of the version to be updated. Can be specified by environment variable JIRA_NEW_VERSION_NAME.')

# Released
parser.add_argument('--released', action=EnvDefault, envvar='JIRA_VERSION_RELEASED', type=bool, help='Indicates that the version is released. Can be specified by environment variable JIRA_VERSION_RELEASED. Default value is false.')

# Archived
parser.add_argument('--archived', action=EnvDefault, envvar='JIRA_VERSION_ARCHIVED', type=bool, help='Indicates that the version is archived. Can be specified by environment variable JIRA_VERSION_ARCHIVED. Default value is false.')

# Url
parser.add_argument('--url', action=EnvDefault, envvar='JIRA_URL', type=str, default='https://jira.org', help='The Jira host url. Default value will be https://jira.org')

# API Version
help_api_version='The Jira API version. Default value is 3. Can be specified by environment variable JIRA_API_VERSION. Supports only versions 2 and 3.'
if "JIRA_API_VERSION" in os.environ:
    parser.add_argument('--api-version', type=int, default=os.environ.get("JIRA_API_VERSION"), help=help_api_version)
else:
    parser.add_argument('--api-version', type=int, default=3, choices=[2, 3], help=help_api_version)

args = parser.parse_args()

if args.api_version != 2 and args.api_version != 3:
    exit(parser.print_usage())

auth = HTTPBasicAuth(args.user, args.password)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    'projectId': args.project
}

# Include description
if args.description != None:
    data['description'] = args.description

# Include released
if args.released != None:
    data['released'] = args.released
    # If released
    if args.released:
        data['userReleaseDate'] = datetime.today().strftime('%d/%b/%y')

# Include archived
if args.archived != None:
    data['archived'] = args.archived

restMethod = "POST"

# Construct URL
if args.update:
    # Update needs to be a PUT request
    restMethod = "PUT"

    # Fetch Version Id
    params = {
        'query': args.version,
        'maxResults': 1
    }

    versionId = None
    getVersionIdUrl = ('%(url)s/rest/api/%(api_version)s/project/%(project)s/version' %{'url': args.url, 'api_version': args.api_version, 'project': args.project})

    try:
        response = requests.request(
            "GET",
            getVersionIdUrl,
            params=params,
            headers=headers,
            auth=auth
        )
        response.raise_for_status()
        # access Json content
        jsonResponse = response.json()
        if jsonResponse["values"] and jsonResponse["values"][0] and jsonResponse["values"][0]["id"]:
            versionId = jsonResponse["values"][0]["id"]
    except HTTPError as http_err:
        print('HTTP error occurred: {error}' %{'error': http_err})
        exit(10)
    except Exception as err:
        print('Other error occurred: {error}' %{'error': err})
        exit(10)

    if versionId == None:
        print(parser.print_usage())
        exit('Unable to retrieve version ID for %(version)s.' %{'version': args.version})

    if args.new_version != None:
        data['name'] = args.new_version
    api_url = ('%(url)s/rest/api/%(api_version)s/version/%(version)s' %{'url': args.url, 'api_version': args.api_version, 'version': versionId})
else:
    data['name'] = args.version
    data['startDate'] = datetime.today().strftime('%Y-%m-%d')
    api_url = ('%(url)s/rest/api/%(api_version)s/version' %{'url': args.url, 'api_version': args.api_version})

try:
    payload = json.dumps(data)
    print("\nWill request to %(url)s" %{'url': api_url})
    print("\nPayload:")
    print(payload)

    response = requests.request(
        restMethod,
        api_url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print('\nResponse:')
    if response.ok:
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    else:
        print("Oops! Something went wrong.")
        print(response)
        exit(10)
except HTTPError as http_err:
    print('HTTP error occurred: {error}' %{'error': http_err})
    exit(10)
except Exception as err:
    print('Other error occurred: {error}' %{'error': err})
    exit(10)
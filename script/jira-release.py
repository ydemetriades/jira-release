#!/usr/bin/env python
from ast import parse
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

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

### Required Arguments
parser = argparse.ArgumentParser( description='Create Jira versions easily', epilog="And that's how we create Jira versions easily!")
parser.add_argument('--version', '-v', action=EnvDefault, envvar='JIRA_VERSION_NAME', type=str, required=True, help='The unique name of the version. Can be specified by environment variable JIRA_VERSION_NAME.')
parser.add_argument('--project', '-p', action=EnvDefault, envvar='JIRA_PROJ', type=int, required=True, help='The ID of the project to which this version is attached.')
parser.add_argument('--user', '-u', action=EnvDefault, envvar='JIRA_AUTH_USER', type=str, required=True, help='The Jira authentication user email.')
parser.add_argument('--password', action=EnvDefault, envvar='JIRA_AUTH_PASSWORD', type=str, required=True, help='Jira API Authorization Password / API Token.')

### Optional Arguments
parser.add_argument('--description', '-d', action=EnvDefault, envvar='JIRA_VERSION_DESCRIPTION', default='', type=str, help='The description of the version. Default value is an empty string.')

# Should update instead of create
help_update='Indicates whether to update or create the version. Can be specified by environment variable JIRA_VERSION_UPDATE. Default value is false.'
if "JIRA_VERSION_UPDATE" in os.environ:
    parser.add_argument('--update', type=bool, default=os.environ.get("JIRA_VERSION_UPDATE"), help=help_update)
else:
    parser.add_argument('--update', action='store_true', help=help_update)

# Released
help_released='Indicates that the version is released. Can be specified by environment variable JIRA_VERSION_RELEASED. Default value is false.'
if "JIRA_VERSION_RELEASED" in os.environ:
    parser.add_argument('--released', type=bool, default=os.environ.get("JIRA_VERSION_RELEASED"), help=help_released)
else:
    parser.add_argument('--released', action='store_true', help=help_released)

# Archived
help_archived='Indicates that the version is archived. Can be specified by environment variable JIRA_VERSION_ARCHIVED. Default value is false.'
if "JIRA_VERSION_ARCHIVED" in os.environ:
    parser.add_argument('--archived', type=bool, default=os.environ.get("JIRA_VERSION_ARCHIVED"), help=help_archived)
else:
    parser.add_argument('--archived', action='store_true', help=help_archived)

# Url
parser.add_argument('--url', action=EnvDefault, envvar='JIRA_URL', type=str, default='https://jira.org', help='The Jira host url. Default value will be https://jira.org')

# API Version
help_api_version='The Jira API version. Default value is 3. Can be specified by environment variable JIRA_API_VERSION. Supports only version 2 and 3.'
if "JIRA_API_VERSION" in os.environ:
    parser.add_argument('--api-version', type=int, default=os.environ.get("JIRA_API_VERSION"), help=help_api_version)
else:
    parser.add_argument('--api-version', type=int, default=3, choices=[2, 3], help=help_api_version)

args = parser.parse_args()

if args.api_version != 2 and args.api_version != 3:
    exit(parser.print_usage())

jira_version_date = datetime.today().strftime('%Y-%m-%d')

auth = HTTPBasicAuth(args.user, args.password)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    'description': args.description,
    'name': args.version,
    'projectId': args.project,
    'released': args.released,
    "archived": args.archived,
}

# If released
if args.released:
    data['userReleaseDate'] = jira_version_date

# Construct URL
if args.update:
    api_url = ('%(url)s/rest/api/%(api_version)s/version/%(version)s' %{'url': args.url, 'api_version': args.api_version, 'version': args.version})
else:
    data['startDate'] = jira_version_date
    api_url = ('%(url)s/rest/api/%(api_version)s/version' %{'url': args.url, 'api_version': args.api_version})

payload = json.dumps(data)

print('\nSending request:')
print(api_url)
print('\nBODY:')
print(data)

response = requests.request(
   "POST",
   api_url,
   data=payload,
   headers=headers,
   auth=auth
)

print('\nResponse:')
print(response)
print(response.text)
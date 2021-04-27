#!/usr/bin/env python
import os
import requests
from datetime import datetime

# Component
jira_component_name = os.getenv('JIRA_COMPONENT_NAME')

# Version
jira_version_name = os.getenv('JIRA_VERSION_NAME')

# Project
jira_project = os.getenv('JIRA_PROJ')

#Authentication
auth_user = os.getenv('JIRA_AUTH_USER')
auth_password = os.getenv('JIRA_AUTH_PASSWORD')

if jira_component_name is None:
    print("Component Name Variable [JIRA_COMPONENT_NAME] is not defined.")
    exit(2)    

if jira_version_name is None:
    print("Version Name Variable [JIRA_VERSION_NAME] is not defined.")
    exit(2)
    
if jira_project is None:
    print("Jira Project Environment Variable [JIRA_PROJ] is not defined.")
    exit(2)

if auth_user is None:
    print("Authentication User Environment Variable [JIRA_AUTH_USER] is not defined.")
    exit(2)
    
if auth_password is None:
    print("Authentication Password Environment Variable [JIRA_AUTH_PASSWORD] is not defined.")
    exit(2)

jira_version_date = datetime.today().strftime('%d/%b/%Y')

jira_url = os.getenv('JIRA_URL', 'https://jira.org')

jira_version_release_env = os.getenv('JIRA_VERSION_RELEASED', 'false')
jira_version_release = True

if jira_version_release_env == 'false':
    jira_version_release = False

jira_version_description =os.getenv('JIRA_VERSION_DESCRIPTION', 'Version {}'.format(jira_version_name))
jira_component_description=os.getenv('JIRA_COMPONENT_DESCRIPTION')

print('Will Attempt to create version [{}] for project [{}] '.format(jira_version_name, jira_project))

jira_api_version = os.getenv('JIRA_API_VERSION', '2')


if jira_api_version == '2':
    data = {
        'description': jira_component_description,
        'name': jira_component_name,
        'project': jira_project,        
    }
    
    # Construct URL
    api_url = ('%(url)s/rest/api/2/component' % {'url': jira_url})
    
    print('Sending request to:')
    print(api_url)
    print('with body')
    print(componentData)

    # Post build status to CI build
    response = requests.post(api_url, auth=(auth_user, auth_password), json=componentData)

    print('Response:')
    print(response)
    print(response.text)

    data = {
        'description': jira_version_description,
        'name': jira_version_name,
        'userReleaseDate': jira_version_date,
        'project': jira_project,
        'released': jira_version_release
    }

    # Construct Version creation URL
    api_url = ('%(url)s/rest/api/2/version' % {'url': jira_url})

    print('Sending request to:')
    print(api_url)
    print('with body')
    print(data)

    # Post build status to CI build
    response = requests.post(api_url, auth=(auth_user, auth_password), json=data)

    print('Response:')
    print(response)
    print(response.text)

    if response:
        exit(0)
    else:
        exit(1)

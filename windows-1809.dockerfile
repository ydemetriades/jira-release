# escape=`
FROM mcr.microsoft.com/powershell:nanoserver-1809
LABEL maintainer="yiannis.demetriades@gmail.com"

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

COPY scripts/ /

RUN Invoke-WebRequest -UseBasicParsing https://chocolatey.org/install.ps1 | Invoke-Expression; `
    choco install -y python --version 3.6.4; 
    
RUN setx /M PATH $($Env:PATH + ';C:\Python36')
RUN python get-pip.py; pip install --no-cache-dir requests

ENTRYPOINT ["python", "/jira-release.py"]
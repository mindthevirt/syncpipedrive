# Sync Pipedrive with Zendesk

This script (`syncpipedrive.py`) allows you to synchronize your accounts & contacts from Pipedrive to Zendesk.


# Getting Started

These instructions will get you running with the project.

### Prerequisites

What things you need to install the software and how to install them

```
Python 2.x with the following library installed:
requests==2.18.2
```
## Creating your own config.json
Use the config.json below as a template and modify its values to match your credentials and configuration.

```
{
  "zendesk": {
    "enduserurl": "https://{subdomain}.zendesk.com/api/v2/users.json?role\[\]=end-user",
    "orgurl": "https://{subdomain}.zendesk.com/api/v2/organizations.json",
    "username": "",
    "apikey": "",
    "url": "{subdomain}.zendesk.com"
  },
  "pipedrive": {
    "apikey": ""
  }
}
```

 - Zendesk API key:
   https://support.zendesk.com/hc/en-us/articles/226022787-Generating-a-new-API-token-

 - Pipedrive API key:
   https://support.pipedrive.com/hc/en-us/articles/207344545-How-to-find-your-personal-API-key

## Running the sync
Upon running ```python syncpipedrive.py```, status messages will be printed to the terminal window:
```
Start sync of organizations from pipedrive to zendesk
Synchronized all organizations from pipedrive to zendesk
Start sync of persons from pipedrive to zendesk
Synchronized all contacts from pipedrive to zendesk
Sync took 0:21:00.792935
```

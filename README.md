# G-Drive recursive copy
A very small python package to recursively copy a folder in Google Drive to another folder in Google Drive.

## Rationale
Google does not support changing ownership on files. Therefore files cannot be moved from a personal Google Drive to a business account, nor to team drives.

Google does support sharing a folder from a personal account to a business account and then manually copying files. Google does not support recursively copying folders. This script does the recursing into folders and copying files into the new folders.

## Installation
At the moment you should download and unzip this package and install its requirements.

Easiest / tidiest is to create a virtual environment in the directory where you've unzipped the files. Commands below create the venv in a directory named "venv":
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
## Usage
At the moment there is no CLI script yet. Therefore, you must use the python CLI or write an small script to launch the recurse_copy() calls per example below.

You can find the folder ID's in the address bar of your browser when the folder is open in your Google Drive. The address should have the form of ```https://drive.google.com/drive/folders/<folder_id>```

```
$ python
Python 3.7.2 (default, Jan 10 2019, 23:51:51)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from drive_migration.g_api_utils import get_api_resource
>>> from drive_migration.folder_copy import recurse_copy
>>> api = get_api_resource()
>>> recurse_copy(api, <source folder id>, <target folder id>)
```
## Security note
This script requires full access to your Google Drive. The acces tokens are stored on your hard drive, in the location where you run these scripts, probably where you've unzipped them.

Make sure they are a bit safe since for now they are not in some form of secure storage. You should worry about access tokens with full access to your Google Drive.

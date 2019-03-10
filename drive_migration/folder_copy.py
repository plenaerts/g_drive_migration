"""
Logic for copying files and folders in G-Drive.
"""
import logging


def create_folder(api, name, parent_id):
    """Create and return a folder.

    Parameters:
    * api:
    * name: name of the folder to create
    * parent_id: name of the parent to create the folder in

    Returns the folders representation.
    """
    logging.info('Creating folder ' + name + ' in ' + parent_id)
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id],
    }
    folder = api.files().create(body=file_metadata).execute()
    logging.info('Created folder id is ' + folder['id'])
    return folder


def copy_file(api, src, parent_id):
    """Create a copy of a file to a target folder and return the file.

    Parameters:
    * api: the Google drive API resource object to use
    * src: the representation of the file to copy - Not the file's ID
    * parent_id: the id of the parent to use for the new file

    Returns the new file representation.
    """
    logging.info('Copying file ' + src['id'] + ' to folder ' + parent_id)
    tgt_body = {"parents": [parent_id],
                'name': src['name']}
    tgt = api.files().copy(fileId=src['id'], body=tgt_body).execute()
    logging.info('Copied file id is ' + tgt['id'])
    return tgt


def recurse_copy(api, src_folder_id, parent_folder_id):
    """Recurse through a folder structure copy it with all items to target.

    Parameters:
    * api: the Google drive API.
    * src_folder_id: id of the source folder. Not of a file!
    * parent_id: id of the target folder.

    Raises a TypeError if the src_folder_id is not a folder.
    """
    logging.info('Starting to recursively copy source folder ' +
                  src_folder_id + ' to target folder with id ' +
                  parent_folder_id)
    src_folder = api.files().get(fileId=src_folder_id).execute()
    if src_folder['mimeType'] != 'application/vnd.google-apps.folder':
        raise TypeError('G-drive source folder file with id ' + src_folder_id +
                        ' is not a folder!')
    parent_folder = api.files().get(fileId=parent_folder_id).execute()
    if parent_folder['mimeType'] != 'application/vnd.google-apps.folder':
        raise TypeError('G-drive target folder file with id ' +
                        parent_folder_id + ' is not a folder!')

    target_folder = create_folder(api, src_folder['name'], parent_folder_id)
    res = api.files().list(
            orderBy='folder,name',
            q='\'' + src_folder_id + '\' in parents').execute()

    # Loop through all files. If we find a folder we recurse into it by calling
    # this function again.
    for item in res['files']:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            logging.info('Found folder ' + item['name'])
            recurse_copy(api, item['id'], target_folder['id'])
        else:
            logging.info('Found file id ' + item['id'] + ' ' + item['name'])
            copy_file(api, item, target_folder['id'])

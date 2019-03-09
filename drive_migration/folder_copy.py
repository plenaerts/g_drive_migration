import logging


def create_folder(drive_service, name, parent_id):
    """Create and return a folder."""
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id],
    }
    folder = drive_service.files().create(body=file_metadata).execute()
    return folder


def copy_file(drive_service, src, parent_id):
    """Create a copy of a file to a target folder and return the file."""
    logging.debug('Copying file ' + src['id'] + ' to folder ' + parent_id)
#    src = drive_service.files().get(fileId=src_id).execute()
    tgt_body = {"parents": [parent_id],
                'name': src['name']}
    tgt = drive_service.files().copy(fileId=src['id'], body=tgt_body).execute()
    logging.debug('Copied file id is ' + tgt['id'])
    return tgt


def recurse_copy(drive_service, src_id, parent_id):
    """Recurse through a folder structure copy it with all items to target.

    Parameters:
    * drive_service: the Google drive API.
    * src_id: id of the source folder.
    * parent_id: id of the target folder.
    """
    src_folder = drive_service.files().get(fileId=src_id).execute()
    target_folder = create_folder(drive_service, src_folder['name'], parent_id)
    res = drive_service.files().list(
            orderBy='folder,name',
            q='\'' + src_id + '\' in parents').execute()
    for item in res['files']:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            logging.debug('Found folder ' + item['name'])
#            folder = create_folder(drive_service,
#                                   item['name'],
#                                   target_folder['id'])
            recurse_copy(drive_service, item['id'], target_folder['id'])
        else:
            logging.debug('Found file id ' + item['id'] + ' ' + item['name'])
            copy_file(drive_service, item, target_folder['id'])

import logging


def create_folder(drive_service, name):
    """Create and return a folder."""
    file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file


def copy_file(drive_service, src_id, parent_id):
    """Create a copy of a file to a target folder and return the file."""
    logging.debug('Copying file ' + src_id + ' to folder ' + parent_id)
    src = drive_service.files().get(fileId=src_id).execute()
    tgt_body = {"parents": [parent_id],
                'name': src['name']}
    tgt = drive_service.files().copy(fileId=src_id, body=tgt_body).execute()
    logging.debug('Copied file id is ' + tgt['id'])


def recurse_copy(drive_service, src, tgt):
    """Recurse through a folder structure copy it with all items to target.

    Parameters:
    * drive_service: the Google drive API.
    * src: id of the source folder.
    * tgt: id of the target folder.
    """
    res = drive_service.files().list(
            orderBy='folder,name',
            q='\'' + src + '\' in parents').execute()
    for item in res['files']:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            logging.debug('Found folder ' + item['name'])
            # create folder here
            # recurse again here
        else:
            logging.debug('Found file ' + item['name'])

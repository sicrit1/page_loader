import re
import os
import requests


def download(path_to_download, path_to_save):
    download_data = requests.get(path_to_download)
    path_to_file = urlfy(path_to_download, path_to_save)
    with open(path_to_file, 'w') as f:
        f.write(download_data.text)
    return path_to_file

def urlfy(path_to_download, path_to_save):
    file_name = path_to_download.split('://')[1]
    file_name = re.sub(r"[^\w\s]", '-', file_name) + '.html'
    path_to_file = os.path.join(path_to_save, file_name)
    return path_to_file


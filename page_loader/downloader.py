# -*- coding:utf-8 -*-


import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path


def download(path_to_download, path_to_save):
    download_data = requests.get(path_to_download)
    true_path = urlfy(path_to_download, path_to_save)
    path_to_html= true_path + '.html'
    path_to_files_dir = true_path + '_files'
    Path(path_to_files_dir).mkdir()
    local_html = get_content(download_data.text, path_to_download, path_to_files_dir)
    Path(path_to_html).write_text(local_html)
    return path_to_html


def urlfy(path_to_download, path_to_save):
    path_without_http = path_to_download.split('://')[1]
    suff = Path(path_without_http).suffix
    true_name = re.sub(r"[^\w\s]", '-', str(Path(path_without_http).with_suffix('')))
    if suff != '':
        true_name = f'{true_name}{suff}'
    true_path = os.path.join(path_to_save, true_name)
    return true_path

def get_content(download_data, path_to_download, path_to_files_dir):
    soup = BeautifulSoup(download_data, 'html.parser')
    for tag in soup.find_all('img'):
        full_path_to_content = urljoin(path_to_download, tag.get('src'))
        if urlparse(full_path_to_content).netloc == urlparse(path_to_download).netloc:
            data = requests.get(full_path_to_content, stream=True)
            path_to_save_content = urlfy(full_path_to_content, path_to_files_dir)
            with open(path_to_save_content, 'wb') as f:
                for chunk in data.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(data.content)
            tag['src'] = path_to_save_content
    local_html = soup.prettify(formatter='html5')
    return local_html
        

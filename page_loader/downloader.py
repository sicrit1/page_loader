# -*- coding:utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path


TAGS = ('img')


def download(path_to_download, path_to_save):
    download_data = requests.get(path_to_download)
    right_name = local_name(path_to_download)
    local_name_html = f'{right_name}.html'
    files_dir_name = f'{right_name}_files'
    local_html, link_to_download = get_content(
        download_data.text,
        path_to_download,
        files_dir_name,
    )
    download_content(link_to_download, Path(path_to_save, files_dir_name))
    path_to_local_html = Path(path_to_save, local_name_html)
    Path(path_to_local_html).write_text(local_html)
    return str(path_to_local_html)


def local_name(path_to_download):
    path_without_http = path_to_download.split('://')[1]
    suff = Path(path_without_http).suffix
    true_name = re.sub(
        r"[^\w\s]", '-',
        str(Path(path_without_http).with_suffix('')),
    )
    if suff != '':
        true_name = f'{true_name}{suff}'
    return true_name


def get_content(download_data, path_to_download, files_dir_name):
    soup = BeautifulSoup(download_data, 'html.parser')
    link_to_download = {}
    for tag in soup.find_all(TAGS):
        source = get_source(tag.name)
        full_path_to_content = urljoin(path_to_download, tag.get(source))
        if urlparse(full_path_to_content).netloc == urlparse(path_to_download).netloc:  # noqa E501
            content_name = local_name(full_path_to_content)
            link_to_download[full_path_to_content] = content_name
            tag[source] = Path(files_dir_name, content_name)
    local_html = soup.prettify(formatter='html5')
    return local_html, link_to_download


def get_source(tag):
    source_dic = {
        'img': 'src'
    }
    return source_dic.get(tag)


def download_content(link_to_download, path_to_files_dir):  # noqa: C901
    Path(path_to_files_dir).mkdir()
    for full_path_to_content, path_to_save_content in link_to_download.items():
        try:
            response = requests.get(full_path_to_content, stream=True)
            with open(path_to_save_content, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)

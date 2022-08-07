# -*- coding:utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from page_loader import app_logger
from page_loader.download_content import download_content


TAGS = ('img', 'link', 'script')

logger = app_logger.get_logger(__name__)


def download(path_to_download, path_to_save):
    logger.info(f'Start downloading {path_to_download}')
    download_data = request_http(path_to_download)
    local_name_html = local_name(path_to_download)
    files_dir_name = local_name(path_to_download, is_dir=True)
    path_to_local_html = Path(path_to_save, local_name_html)
    local_html, link_to_download = get_content(
        download_data.text,
        path_to_download,
        files_dir_name,
    )
    download_content(link_to_download, Path(path_to_save, files_dir_name))
    Path(path_to_local_html).write_text(local_html)
    logger.info(f'Finish downloading. Page has been saved to {path_to_save}')
    return str(path_to_local_html)


def request_http(path_to_download):
    download_data = requests.get(path_to_download)
    if download_data.status_code != 200:
        raise Exception(
            'Error. Status code = {}.format(download_data.status_code)'
        )
    return download_data


def local_name(path_to_download, is_dir=False):
    parsed_link = urlparse(path_to_download)
    suff = Path(parsed_link.path).suffix
    true_name = re.sub(
        r"[^\w\s]", '-',
        str(Path(parsed_link.netloc + parsed_link.path).with_suffix('')),
    )
    if is_dir:
        true_name = f'{true_name}_files'
    elif suff != '':
        true_name = f'{true_name}{suff}'
    else:
        true_name = f'{true_name}.html'
    return true_name


def get_content(download_data, path_to_download, files_dir_name):
    soup = BeautifulSoup(download_data, 'html.parser')
    link_to_download = {}
    for tag in soup.find_all(TAGS):
        source = get_source(tag.name)
        full_path_to_content = urljoin(path_to_download, tag.get(source))
        if urlparse(full_path_to_content).netloc == urlparse(path_to_download).netloc:  # noqa E501
            content_name = local_name(full_path_to_content)
            path_to_saved_content = Path(files_dir_name, content_name)
            link_to_download[full_path_to_content] = content_name
            tag[source] = path_to_saved_content
    local_html = soup.prettify()
    return local_html, link_to_download


def get_source(tag):
    source_dic = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }
    return source_dic.get(tag)

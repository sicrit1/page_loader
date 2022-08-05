# -*- coding:utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import logging
from page_loader import app_logger


TAGS = ('img', 'link', 'script')

logger = app_logger.get_logger(__name__)


def download(path_to_download, path_to_save):
    logger.info(f'Start downloading {path_to_download}')
    download_data = requests.get(path_to_download)
    local_name_html = local_name(path_to_download)
    files_dir_name = local_name(path_to_download, is_dir=True)
    path_to_files_dir = Path(path_to_save, files_dir_name)
    path_to_local_html = Path(path_to_save, local_name_html)
    local_html, link_to_download = get_content(
        download_data.text,
        path_to_download,
        path_to_files_dir,
    )
    download_content(link_to_download, path_to_files_dir)
    Path(path_to_local_html).write_text(local_html)
    logger.info(f'Finish downloading. Page has been saved to {path_to_save}')
    return str(path_to_local_html)


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


def get_content(download_data, path_to_download, path_to_files_dir):
    soup = BeautifulSoup(download_data, 'html.parser')
    link_to_download = {}
    for tag in soup.find_all(TAGS):
        source = get_source(tag.name)
        full_path_to_content = urljoin(path_to_download, tag.get(source))
        if urlparse(full_path_to_content).netloc == urlparse(path_to_download).netloc:  # noqa E501
            content_name = local_name(full_path_to_content)
            path_to_save_content = Path(path_to_files_dir, content_name)
            link_to_download[full_path_to_content] = path_to_save_content
            tag[source] = path_to_save_content
    local_html = soup.prettify()
    return local_html, link_to_download


def get_source(tag):
    source_dic = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }
    return source_dic.get(tag)


def download_content(link_to_download, path_to_files_dir):  # noqa: C901
    logger.info(f'Start downloading local resources')
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
    logger.info(
        f'Finish downloading resources.'
        f'Resources have been saved to {path_to_save_content}'
    )

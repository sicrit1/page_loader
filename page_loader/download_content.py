# -*- coding:utf-8 -*-


import requests
from pathlib import Path
from page_loader import app_logger
from progress.bar import IncrementalBar


logger = app_logger.get_logger(__name__)


def download_content(link_to_download, path_to_files_dir):  # noqa: C901
    logger.info(f'{"Start downloading local resources"}')
    Path(path_to_files_dir).mkdir()
    progress_bar = IncrementalBar(
        'Downloading', max=len(link_to_download), suffix='%(percent).1f%%'
    )

    for full_path_to_content, content_name in link_to_download.items():
        try:
            response = requests.get(full_path_to_content, stream=True)
            with open(Path(path_to_files_dir, content_name), 'wb') as f:
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
        progress_bar.next()

    progress_bar.finish()
    logger.info(
        f'Finish downloading resources.'
        f'Resources have been saved to {path_to_files_dir}'
    )

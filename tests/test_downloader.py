import os
from pathlib import Path
from page_loader.downloader import download, local_name
from bs4 import BeautifulSoup
import pytest


URL_TO_RESPONSE = {
    'html': 'https://ru.hexlet.io/courses',
    'img': 'https://ru.hexlet.io/assets/professions/nodejs.png',
}
TEST_FILE_NAME = {
    'html': 'test_file_to_download.html',
    'img': 'test_picture.png',
    'changed_html': 'test_file_changed.html',
}


def get_path(name):
    path_to_result = os.path.join('tests/fixtures', name)
    return path_to_result


def test_downloader(tmpdir, requests_mock):
    path_to_html = get_path(TEST_FILE_NAME['html'])
    download_html = (Path(path_to_html)).read_bytes()
    path_to_img = get_path(TEST_FILE_NAME['img'])
    download_img = (Path(path_to_img)).read_bytes()
    requests_mock.get(URL_TO_RESPONSE['html'], content=download_html)
    requests_mock.get(URL_TO_RESPONSE['img'], content=download_img)

    full_result_path = download(URL_TO_RESPONSE['html'], tmpdir)
    result_data = (Path(full_result_path)).read_bytes()
    path_to_expected_data = get_path(TEST_FILE_NAME['changed_html'])
    expected_data = (Path(path_to_expected_data)).read_bytes()
    expected_html = BeautifulSoup(expected_data, 'html.parser').prettify(formatter='html5')  # noqa: E501
    result_html = BeautifulSoup(result_data, 'html.parser').prettify(formatter='html5')  # noqa: E501
    assert expected_html == result_html


@pytest.mark.parametrize(
    'path_to_download, result',
    [
        (
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses',
        ),
    ],
)
def test_local_name(path_to_download, result):
    test_path = local_name(path_to_download)
    assert result == test_path

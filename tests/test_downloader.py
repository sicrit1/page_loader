import os
from pathlib import Path
from page_loader.downloader import download, local_name
from bs4 import BeautifulSoup
import pytest


URL_TO_RESPONSE = {
    'html': 'https://ru.hexlet.io/courses',
    'img': '/assets/professions/nodejs.png',
    'script': 'https://ru.hexlet.io/packs/js/runtime.js',
    'link': '/assets/application.css',
}
TEST_FILE_NAME = {
    'html': 'test_file_to_download.html',
    'img': 'test_picture.png',
    'script': 'test_file_script.js',
    'link': 'test_file_link.css',
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
    path_to_link = get_path(TEST_FILE_NAME['link'])
    download_link = (Path(path_to_link)).read_bytes()
    path_to_script = get_path(TEST_FILE_NAME['script'])
    download_script = (Path(path_to_script)).read_bytes()
    requests_mock.get(URL_TO_RESPONSE['html'], content=download_html)
    requests_mock.get(URL_TO_RESPONSE['img'], content=download_img)
    requests_mock.get(URL_TO_RESPONSE['link'], content=download_link)
    requests_mock.get(URL_TO_RESPONSE['script'], content=download_script)

    full_result_path = download(URL_TO_RESPONSE['html'], tmpdir)
    result_data = Path(full_result_path).read_bytes()
    path_to_expected_data = get_path(TEST_FILE_NAME['changed_html'])
    expected_data = Path(path_to_expected_data).read_bytes()
    expected_html = BeautifulSoup(expected_data, 'html.parser').prettify()
    result_html = BeautifulSoup(result_data, 'html.parser').prettify()
    assert expected_html == result_html


@pytest.mark.parametrize(
    'path_to_download, result, is_dir',
    [
        (
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses.html',
            False,
        ),
        (
            'https://ru.hexlet.io/courses/runtime.js',
            'ru-hexlet-io-courses-runtime.js',
            False,
        ),
        (
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files',
            True,
        ),


    ],
)
def test_local_name(path_to_download, result, is_dir):
    test_path = local_name(path_to_download, is_dir)
    assert result == test_path


@pytest.mark.parametrize('status_code', [
    400, 401, 403, 404, 500, 502,
])
def test_status_code(requests_mock, tmpdir, status_code):
    requests_mock.get(URL_TO_RESPONSE['html'], status_code=status_code)
    with pytest.raises(Exception):
        download(URL_TO_RESPONSE['html'], tmpdir)

import os
from pathlib import Path
from page_loader.downloader import download, urlfy
import pytest

TEST_FILE = 'test_file_to_download.html'
URL_TO_RESPONSE = 'https://ru.hexlet.io/courses'
DIR_TO_SAVE = 'tests/fixtures'


def get_path(name):
    path_to_result = os.path.join('tests/fixtures', name)
    return path_to_result


def test_downloader(tmpdir, requests_mock):
    path_to_download_file = get_path(TEST_FILE)
    download_data = (Path(path_to_download_file)).read_bytes()
    requests_mock.get(URL_TO_RESPONSE, content=download_data)

    full_result_path = download(URL_TO_RESPONSE, tmpdir)
    result = (Path(full_result_path)).read_bytes()
    assert result == download_data


@pytest.mark.parametrize(
    'path_to_download, path_to_save, result',
    [
        (
            'https://ru.hexlet.io/courses',
            '/var/tmp',
            '/var/tmp/ru-hexlet-io-courses.html',
        ),
    ],
)
def test_urlfy(path_to_download, path_to_save, result):
    test_path = urlfy(path_to_download, path_to_save)
    assert result == test_path

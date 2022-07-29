import argparse
import os
from page_loader.downloader import download


def parser_html():
    pwd_path = os.getcwd()
    parser = argparse.ArgumentParser(
        description='This utility download a page from the Internet'
        'and save it local'
    )
    parser.add_argument(
        'path_to_html',
        type=str,
        help='Input adress to download a html',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=pwd_path,
        help='Input dir for downloaded html',
    )
    args = parser.parse_args()
    print(download(args.path_to_html, args.output))


def main():
    parser_html()


if __name__ == '__main__':
    main()

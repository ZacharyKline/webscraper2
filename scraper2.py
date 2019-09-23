#!/usr/bin/env python3
import sys
import argparse
import requests
import re
from bs4 import BeautifulSoup
from urlparse import urljoin

"""Author: Zachary Kline with help from Alec Stephens for the relative links"""


def find_urls(website):
    req = requests.get(website)
    req = req.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", req)
    urls = set(urls)
    urls = '\n'.join(urls)
    return 'URLS:\n\n {}'.format(urls)


def find_tags(website):
    img_tags = []
    href_tags = []
    req = requests.get(website)
    soup = BeautifulSoup(req.content, features="html.parser")
    href = soup.find_all('a')
    for href_link in href:
        href_paths = urljoin(website, str(href_link.get('href')))
        if href_paths not in href_tags:
            href_tags.append(href_paths)
    img = soup.find_all('img')
    for img_link in img:
        img_paths = urljoin(website, str(img_link.get('img')))
        if img_paths not in img_tags:
            img_tags.append(img_paths)
    img_tags = '\n'.join(img_tags)
    href_tags = '\n'.join(href_tags)

    return 'A Tags:\n\n {}\n\n IMG Tags:\n\n {}\n'.format(href_tags, img_tags)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--webs', '-w',  help='Find URLS in a given website')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    parsed_urls = find_urls(parsed_args.webs)
    parsed_tags = find_tags(parsed_args.webs)
    print('Full Tags:\n\n {} \n Partial Tags:\n\n {}'.format(
        parsed_urls, parsed_tags))


if __name__ == '__main__':
    main(sys.argv[1:])

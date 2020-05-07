import argparse
import math
from pathlib import Path
import sys
from typing import Any, Dict, List
import requests


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(
        description='Provides information about a git repository hosted on '
                    'GitHub without cloning it.')
    parser.add_argument('GitHub_URL', type=str,
                        help='A GitHub URL for a repo to analyze')
    args = parser.parse_args()
    return args


# Function to check the internet connection
def connection(url='http://www.google.com/', timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        print("You're connected to internet\n")
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
            e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def main(args: argparse.Namespace) -> None:
    url = args.GitHub_URL
    url_slice = url.split('/')
    org = url_slice[3]
    repo_name = url_slice[4]
    url = f'https://api.github.com/repos/{org}/{repo_name}'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        print(r.json())


if __name__ == '__main__':
    args = parse_arguments()
    main(args)

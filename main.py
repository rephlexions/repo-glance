import argparse
import math
import sys
from typing import Any, Dict, List
import requests
from rich.console import Console

console = Console()


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(
        description='Provides information about a git repository hosted on '
                    'GitHub without cloning it.')
    parser.add_argument('GitHub_URL', type=str,
                        help='A GitHub URL for a repo to analyze')
    args = parser.parse_args()
    return args


def connection(url='http://www.google.com/', timeout=5) -> True:
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


def num_kilobytes_to_size_str(size_bytes: int) -> str:
    size_name = ("KiB", "MiB", "GiB", "TiB")
    x = int(math.floor(math.log(size_bytes, 1024)))
    return f"{size_bytes / (1024 ** x):.2f} {size_name[x]}"


def get_languages(lang_url: str) -> List[str]:
    languages = []
    req = requests.get(lang_url).json()
    for i in req:
        languages.append(i)
    return languages


def get_license(license: Dict[str, str]) -> str:
    for k, v in license.items():
        if k == "name":
            return v


def print_info(repo_info: Dict[str, str]) -> str:
    console.print("Basic info about the repository: \n",
                  style="magenta 14")
    print("Name: " + repo_info['name'])
    print(f"Repository Size: {num_kilobytes_to_size_str(repo_info['size'])}")
    print(f"Repository License: {get_license(repo_info['license'])}")
    print(f"Repository Description: {repo_info['description']}")

    print("Languages used:")
    print(','.join(get_languages(repo_info['languages_url'])))

    print("Repository Statistics:")
    print(f"Forks: {repo_info['forks']}")
    print(f"Watchers: {repo_info['watchers']}")
    print(f"Open Issues: {repo_info['open_issues']}")
    print(f"Total Stars: {repo_info['stargazers_count']}")

    print("GIT:   " + repo_info['git_url'])
    print("SSH:   " + repo_info['ssh_url'])
    print("SVN:   " + repo_info['svn_url'])
    print("Clone: " + repo_info['clone_url'])


def main(args: argparse.Namespace) -> None:
    if connection():
        url = args.GitHub_URL
        url_slice = url.split('/')
        org = url_slice[3]
        repo_name = url_slice[4]
        url = f'https://api.github.com/repos/{org}/{repo_name}'
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            print_info(req.json())


if __name__ == '__main__':
    args = parse_arguments()
    main(args)

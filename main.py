import argparse
import math
import sys
from typing import Any, Dict, List
import requests
from rich.console import Console
from rich.table import Table
from rich import box

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
        console.print("You're connected to internet\n", style="bright_green")
        return True
    except requests.HTTPError as e:
        console.print("Checking internet connection failed, status code {0}.".format(
            e.response.status_code), style="bright_red")
    except requests.ConnectionError:
        console.print("No internet connection available.", style="bright_red")
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
                  style="#ffd31d")

    console.print("Name:", style="#6fe7dd", end='')
    console.print(repo_info['name'], style="#3490de")

    console.print("Repository Size:", style="#6fe7dd", end='')
    console.print(
        f"{num_kilobytes_to_size_str(repo_info['size'])}", style="#3490de")

    console.print("Repository License: ", style="#6fe7dd", end='')
    console.print(f"{get_license(repo_info['license'])}", style="#3490de")

    console.print("Repository Description:", style="#6fe7dd")
    console.print(f"{repo_info['description']}", style="#3490de")

    console.print("Languages used: ", style="#6fe7dd")
    console.print(', '.join(get_languages(
        repo_info['languages_url'])), style="#3490de")

    stats_table = Table(title="Repository Statistics:",
                        style="#6639a6", title_style="#6fe7dd", box=box.SQUARE)
    stats_table.add_column("Statistics", justify="right",
                           style="#6fe7dd", no_wrap=True)
    stats_table.add_column("Count", justify="right", style="green")
    stats_table.add_row("Forks", f"{repo_info['forks']}")
    stats_table.add_row("Watchers", f"{repo_info['watchers']}")
    stats_table.add_row("Open Issues", f"{repo_info['open_issues']}")
    stats_table.add_row("Total Stars", f"{repo_info['stargazers_count']}")
    console.print(stats_table)

    url_table = Table(title="URLs of the repository",
                      style="#6639a6", title_style="#6fe7dd", box=box.SQUARE)
    url_table.add_column("Type", justify="right",
                         style="#6fe7dd", no_wrap=True)
    url_table.add_column("URL", justify="right", style="green")
    url_table.add_row("GIT",  f"{repo_info['git_url']}")
    url_table.add_row("SSH",  f"{repo_info['ssh_url']}")
    url_table.add_row("SNV",  f"{repo_info['svn_url']}")
    url_table.add_row("Clone",  f"{repo_info['clone_url']}")
    console.print(url_table)


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

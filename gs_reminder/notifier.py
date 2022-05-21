import json
import os
from pathlib import Path
from typing import List

import click

from .bridge import BridgeUsername
from .github import api as github_api
from .slack import api as slack_api


def get_bridge_usernames(file_username: str) -> List[BridgeUsername]:
    return list(map(lambda item: BridgeUsername(**item), json.loads(Path(file_username).read_text())))


@click.command(
    help="""GitHub repository's pull requests slack notifier\n
Required environments variables\n
    - GITHUB_TOKEN: Your GitHub Personal Access Token.\n
    - SLACK_URL: Your Slack webhook url."""
)
@click.option(
    "--repo",
    "-r",
    type=str,
    help="GitHub repository name (owner/repo).",
    required=True,
)
@click.option(
    "--file-username",
    "-u",
    type=str,
    help="Corresponding files for GitHub and Slack usernames. (see. example in README.md)",
    required=True,
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=20,
    help="Number of Pull Requests to notify Slack.",
    required=True,
)
def main(repo: str, file_username: str, limit: int) -> None:
    if limit > 20:
        raise ValueError("Cannot set more than 20 items.")

    gh = github_api.Client(token=os.environ["GITHUB_TOKEN"])
    # get pull requests
    pulls = gh.get_pulls(repo=repo, limit=limit)
    # get total pull requests count
    total_pulls = gh.get_total_pulls(repo=repo)
    # get GitHub and GitHub bridge username
    usernames = get_bridge_usernames(file_username=file_username)

    # send slack
    sl = slack_api.Client(usernames=usernames)
    sl.post(repo=repo, pulls=pulls, total_pulls=total_pulls)


if __name__ == "__main__":
    main()

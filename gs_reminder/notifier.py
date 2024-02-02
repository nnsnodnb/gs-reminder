import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import click

from . import __version__
from .bridge import BridgeUsername
from .error import SlackException
from .github import api as github_api
from .slack import api as slack_api


def get_bridge_usernames(file_username: Optional[str]) -> List[BridgeUsername]:
    if file_username is None:
        return []
    return list(
        map(
            lambda item: BridgeUsername(**item),
            json.loads(Path(file_username).read_text()),
        )
    )


@click.version_option(version=__version__)
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
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=20,
    help="Number of Pull Requests to notify Slack.",
    required=True,
)
@click.option(
    "--icon",
    "-i",
    is_flag=True,
    type=bool,
    default=False,
    help="Give GitHub icons to Slack notifications.",
    required=False,
)
@click.option(
    "--exclude-users",
    "-eu",
    type=str,
    default=[],
    multiple=True,
    help="GitHub users to remove from reviewers upon notification.",
    required=False,
)
def main(repo: str, file_username: Optional[str], limit: int, icon: bool, exclude_users: List[str]) -> None:
    if limit > 20:
        raise ValueError("Cannot set more than 20 items.")

    gh = github_api.Client(github_token=os.environ["GITHUB_TOKEN"])
    # get pull requests
    pulls = gh.get_pulls(repo=repo, limit=limit)
    # get total pull requests count
    total_pulls = gh.get_total_pulls(repo=repo)
    # get GitHub and GitHub bridge username
    usernames = get_bridge_usernames(file_username=file_username)

    # send slack
    sl = slack_api.Client(usernames=usernames, icon=icon, exclude_users=exclude_users)
    try:
        sl.post(repo=repo, pulls=pulls, total_pulls=total_pulls)
    except SlackException as e:
        print(f"Slack Exception {e.response['detail']}", end=" ")
        sys.exit(1)


if __name__ == "__main__":
    main()

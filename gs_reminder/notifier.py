import json
import os
from pathlib import Path
from typing import List

import click

from .bridge import BridgeUsername
from .github import api as github_api
from .github.models.pull_request import PullRequest
from .slack import api as slack_api


def get_pulls(repo: str) -> List[PullRequest]:
    client = github_api.Client(token=os.getenv("GITHUB_TOKEN"))
    # get pull requests
    pulls = client.get_pulls(repo=repo)
    # filter pull requests
    pulls = list(filter(lambda pr: not pr.draft, pulls))

    return pulls


def get_bridge_usernames(file_username: str) -> List[BridgeUsername]:
    return list(map(lambda item: BridgeUsername(**item), json.loads(Path(file_username).read_text())))


def send_block(repo: str, pulls: List[PullRequest], usernames: List[BridgeUsername]) -> None:
    client = slack_api.Client(usernames=usernames)
    client.post(repo=repo, pulls=pulls)


@click.command(
    help="""GitHub repository's pull requests slack notifier\n
Required environments variables\n
    - GITHUB_TOKEN: Your GitHub Personal Access Token.\n
    - SLACK_URL: Your Slack webhook url."""
)
@click.option(
    "-r",
    "--repo",
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
def main(repo: str, file_username: str) -> None:
    pulls = get_pulls(repo=repo)
    usernames = get_bridge_usernames(file_username=file_username)
    send_block(repo=repo, pulls=pulls, usernames=usernames)


if __name__ == "__main__":
    main()

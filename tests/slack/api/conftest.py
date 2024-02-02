import json
import os
from pathlib import Path
from typing import Generator, List

import pytest

from gs_reminder.bridge import BridgeUsername
from gs_reminder.github.models.pull_request import PullRequest


@pytest.fixture(scope="session", autouse=True)
def slack_url() -> Generator:
    os.environ["SLACK_URL"] = "https://hooks.slack.com/services/AAAAAAAAA/BBBBBBBBBBB/CCCCCCCCCCCCCCCCCCCCCCCC"
    yield
    del os.environ["SLACK_URL"]


@pytest.fixture()
def bridge_usernames() -> List[BridgeUsername]:
    usernames = [BridgeUsername(github=f"user{i}", slack=f"slack.user{i}") for i in range(5)]
    usernames += [
        BridgeUsername(github="octocat", slack="slack.octocat"),
        BridgeUsername(github="other_user", slack="slack.other_user"),
    ]
    return usernames


@pytest.fixture()
def pull() -> PullRequest:
    res_path = Path(__file__).parents[2] / "mock_res" / "pulls.json"
    if not res_path.exists():
        raise FileNotFoundError(f"{res_path} is not found.")
    res_json = json.loads(res_path.read_text())
    return PullRequest(**res_json[0])


@pytest.fixture()
def repo() -> str:
    return "nnsnodnb/gs-reminder"

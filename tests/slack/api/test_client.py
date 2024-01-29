import os

import pytest

from gs_reminder.error import SlackException
from gs_reminder.github.models.user import User
from gs_reminder.slack.api import Client


@pytest.mark.parametrize(
    "user_login, expected",
    [
        ("user1", "@slack.user1"),
        ("user3", "@slack.user3"),
        ("user5", "user5"),
    ],
    ids=["found user1", "found user3", "not found user5"],
)
def test_convert_github_to_slack(user_login, expected, bridge_usernames):
    client = Client(usernames=bridge_usernames, icon=False, exclude_users=[])

    user = User(login=user_login, id=1, type="User", avatar_url="https://example.com")

    username = client._convert_github_to_slack(user)

    assert username == expected


@pytest.mark.parametrize(
    "icon",
    [
        True,
        False,
    ],
    ids=["Enable icon", "Disable icon"],
)
def test_get_section_exists_requested_reviewers(icon, bridge_usernames, pull):
    client = Client(usernames=bridge_usernames, icon=icon, exclude_users=[])

    title_section, reviewer_section = client._get_section(pull=pull)

    assert title_section["type"] == "section"
    assert title_section["text"]["type"] == "mrkdwn"
    assert title_section["text"]["text"] == f"[#{pull.number}] <{pull.html_url}|{pull.title}> (_{pull.user.login}_)"
    assert title_section["accessory"]["type"] == "button"
    assert title_section["accessory"]["text"]["type"] == "plain_text"
    assert title_section["accessory"]["text"]["text"] == "Review"
    assert title_section["accessory"]["url"] == pull.html_url
    assert reviewer_section["type"] == "context"
    assert len(reviewer_section["elements"]) == len(pull.requested_reviewers) + (2 if icon else 1)
    assert reviewer_section["elements"][0]["type"] == "plain_text"
    assert reviewer_section["elements"][0]["text"] == "Waiting on"
    assert reviewer_section["elements"][1]["type"] == "image" if icon else "mrkdwn"
    if icon:
        assert reviewer_section["elements"][1]["image_url"] == pull.requested_reviewers[0].avatar_url
        assert reviewer_section["elements"][1]["alt_text"] == pull.requested_reviewers[0].login
        assert reviewer_section["elements"][2]["type"] == "mrkdwn"
        assert reviewer_section["elements"][2]["text"] == "@slack.other_user"
    else:
        assert reviewer_section["elements"][1]["type"] == "mrkdwn"
        assert reviewer_section["elements"][1]["text"] == "@slack.other_user"


def test_get_section_empty_requested_reviewers(pull):
    client = Client(usernames=[], icon=True, exclude_users=[])
    pull.requested_reviewers = []

    title_section, reviewer_section = client._get_section(pull=pull)

    assert title_section["type"] == "section"
    assert title_section["text"]["type"] == "mrkdwn"
    assert title_section["text"]["text"] == f"[#{pull.number}] <{pull.html_url}|{pull.title}> (_{pull.user.login}_)"
    assert title_section["accessory"]["type"] == "button"
    assert title_section["accessory"]["text"]["type"] == "plain_text"
    assert title_section["accessory"]["text"]["text"] == "Review"
    assert title_section["accessory"]["url"] == pull.html_url
    assert reviewer_section["type"] == "context"
    assert len(reviewer_section["elements"]) == 1
    assert reviewer_section["elements"][0]["type"] == "plain_text"
    assert reviewer_section["elements"][0]["text"] == "Waiting review by anyone."


@pytest.mark.parametrize(
    "total_pulls_is_over",
    [True, False],
    ids=["over", "under"],
)
def test_build_block(bridge_usernames, pull, repo, total_pulls_is_over):
    client = Client(usernames=[], icon=True, exclude_users=[])

    blocks = client._build_block(repo=repo, pulls=[pull], total_pulls=10 if total_pulls_is_over else 1)

    assert blocks[0]["type"] == "section"
    assert blocks[0]["text"]["type"] == "mrkdwn"
    assert blocks[0]["text"]["text"] == f"*Pending review on _<https://github.com/{repo}|{repo}>_*"
    assert blocks[1]["type"] == "section"
    assert blocks[1]["text"]["type"] == "mrkdwn"
    assert blocks[1]["text"]["text"] == f"[#{pull.number}] <{pull.html_url}|{pull.title}> (_{pull.user.login}_)"
    if total_pulls_is_over:
        index = len(blocks) - 2
        assert blocks[index]["type"] == "section"
        assert blocks[index]["text"]["type"] == "mrkdwn"
        assert blocks[index]["text"]["text"] == "Number of remaining: *9*"
        assert blocks[index]["accessory"]["type"] == "button"
        assert blocks[index]["accessory"]["text"]["type"] == "plain_text"
        assert blocks[index]["accessory"]["text"]["text"] == "Watch"
        assert blocks[index]["accessory"]["url"] == f"https://github.com/{repo}/pulls"
    assert blocks[::-1][0]["type"] == "divider"


def test_success_post(requests_mock, pull, repo):
    requests_mock.post(os.getenv("SLACK_URL"), json={})

    client = Client(usernames=[], icon=True, exclude_users=[])

    client.post(repo=repo, pulls=[pull], total_pulls=1)

    assert requests_mock.called
    assert len(requests_mock.request_history) == 1
    assert requests_mock.request_history[0].method == "POST"
    assert requests_mock.request_history[0].url == os.getenv("SLACK_URL")


def test_post_empty_pulls(requests_mock, repo):
    requests_mock.post(os.getenv("SLACK_URL"), json={})

    client = Client(usernames=[], icon=True, exclude_users=[])

    client.post(repo=repo, pulls=[], total_pulls=0)

    assert not requests_mock.called


@pytest.mark.parametrize(
    "status_code, content",
    [
        (400, b"Bad Request"),
        (500, b"Internal Server Error"),
    ],
    ids=["Bad Request", "Internal Server Error"],
)
def test_failure_post(requests_mock, pull, repo, status_code, content):
    requests_mock.post(os.getenv("SLACK_URL"), content=content, status_code=status_code)

    client = Client(usernames=[], icon=True, exclude_users=[])

    with pytest.raises(SlackException) as e:
        client.post(repo=repo, pulls=[pull], total_pulls=1)

    assert requests_mock.called
    assert len(requests_mock.request_history) == 1
    assert requests_mock.request_history[0].method == "POST"
    assert e.value.status_code == status_code
    assert e.value.response == {"detail": content.decode("utf-8")}

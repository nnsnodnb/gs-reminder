import pytest

from gs_reminder.bridge import BridgeUsername


@pytest.mark.parametrize(
    "slack_name, expected",
    [
        ("slack.name", "@slack.name"),
        ("@slack.name", "@slack.name"),
    ],
)
def test_bridge_username(slack_name, expected):
    bridge_username = BridgeUsername(github="octcat", slack=slack_name)

    assert bridge_username.github == "octcat"
    assert bridge_username.slack == expected

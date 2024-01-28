import pytest

from gs_reminder.github.api import Client


@pytest.fixture()
def github_api_client() -> Client:
    return Client("github_token")

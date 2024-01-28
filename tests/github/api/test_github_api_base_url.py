from gs_reminder.github.api import GITHUB_API_BASE_URL


def test_github_api_base_url():
    assert GITHUB_API_BASE_URL == "https://api.github.com"

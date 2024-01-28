import json
from pathlib import Path

import pytest

from gs_reminder.error import GitHubException
from gs_reminder.github.api import GITHUB_API_BASE_URL


def test_success_get_pulls(requests_mock, github_api_client):
    res_path = Path(__file__).parent / "mock_res" / "pulls.json"
    mock_json = json.loads(res_path.read_text())
    requests_mock.get(f"{GITHUB_API_BASE_URL}/repos/username/repo/pulls", json=mock_json, status_code=200)

    res = github_api_client.get_pulls(repo="username/repo", limit=1)

    assert requests_mock.called
    assert len(res) == 1
    assert isinstance(res, list)


@pytest.mark.parametrize(
    "status_code, response",
    [
        (404, {"message": "Not Found"}),
        (422, {"message": "Validation Failed"}),
        (500, {"message": "Internal Server Error"}),
    ],
    ids=["Not Found", "Validation Failed", "Internal Server Error"],
)
def test_failure_get_pulls(requests_mock, github_api_client, status_code, response):
    requests_mock.get(f"{GITHUB_API_BASE_URL}/repos/username/repo/pulls", json=response, status_code=status_code)

    with pytest.raises(GitHubException) as e:
        github_api_client.get_pulls(repo="username/repo", limit=1)

    assert requests_mock.called
    assert e.value.status_code == status_code
    assert e.value.response == response
    assert e.value.detail == "get_pulls"


def test_success_get_total_pulls(requests_mock, github_api_client):
    res_path = Path(__file__).parent / "mock_res" / "search_issues.json"
    mock_json = json.loads(res_path.read_text())
    requests_mock.get(f"{GITHUB_API_BASE_URL}/search/issues", json=mock_json, status_code=200)

    res = github_api_client.get_total_pulls(repo="username/repo")

    assert requests_mock.called
    assert isinstance(res, int)
    assert res == 138


@pytest.mark.parametrize(
    "status_code, response",
    [
        (404, {"message": "Not Found"}),
        (422, {"message": "Validation Failed"}),
        (500, {"message": "Internal Server Error"}),
    ],
    ids=["Not Found", "Validation Failed", "Internal Server Error"],
)
def test_failure_get_total_pulls(requests_mock, github_api_client, status_code, response):
    requests_mock.get(f"{GITHUB_API_BASE_URL}/search/issues", json=response, status_code=status_code)

    with pytest.raises(GitHubException) as e:
        github_api_client.get_total_pulls(repo="username/repo")

    assert requests_mock.called
    assert e.value.status_code == status_code
    assert e.value.response == response
    assert e.value.detail == "get_total_pulls"

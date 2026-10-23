import json
from pathlib import Path

import pytest

from gs_reminder.error import GitHubException
from gs_reminder.github.api import GITHUB_API_BASE_URL


def test_success_get_pulls(httpx2_mock, github_api_client):
    res_path = Path(__file__).parents[2] / "mock_res" / "pulls.json"
    mock_json = json.loads(res_path.read_text())
    httpx2_mock.add_response(
        method="GET",
        url=f"{GITHUB_API_BASE_URL}/repos/username/repo/pulls",
        match_params={"state": "open", "sort": "created", "per_page": 25, "page": 1},
        json=mock_json,
    )

    res = github_api_client.get_pulls(repo="username/repo", limit=1)

    assert len(httpx2_mock.get_requests()) == 1
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
def test_failure_get_pulls(httpx2_mock, github_api_client, status_code, response):
    httpx2_mock.add_response(
        method="GET",
        url=f"{GITHUB_API_BASE_URL}/repos/nnsnodnb/gs-reminder/pulls",
        match_params={"state": "open", "sort": "created", "per_page": 25, "page": 1},
        json=response,
        status_code=status_code,
    )

    with pytest.raises(GitHubException) as e:
        github_api_client.get_pulls(repo="nnsnodnb/gs-reminder", limit=1)

    assert len(httpx2_mock.get_requests()) == 1
    assert e.value.status_code == status_code
    assert e.value.response == response
    assert e.value.detail == "get_pulls"


def test_success_get_total_pulls(httpx2_mock, github_api_client):
    res_path = Path(__file__).parents[2] / "mock_res" / "search_issues.json"
    mock_json = json.loads(res_path.read_text())
    httpx2_mock.add_response(
        method="GET",
        url=f"{GITHUB_API_BASE_URL}/search/issues",
        match_params={"q": "type:pr repo:nnsnodnb/gs-reminder state:open", "per_page": 1},
        json=mock_json,
    )

    res = github_api_client.get_total_pulls(repo="nnsnodnb/gs-reminder")

    assert len(httpx2_mock.get_requests()) == 1
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
def test_failure_get_total_pulls(httpx2_mock, github_api_client, status_code, response):
    httpx2_mock.add_response(
        method="GET",
        url=f"{GITHUB_API_BASE_URL}/search/issues",
        match_params={"q": "type:pr repo:nnsnodnb/gs-reminder state:open", "per_page": 1},
        json=response,
        status_code=status_code,
    )

    with pytest.raises(GitHubException) as e:
        github_api_client.get_total_pulls(repo="nnsnodnb/gs-reminder")

    assert len(httpx2_mock.get_requests()) == 1
    assert e.value.status_code == status_code
    assert e.value.response == response
    assert e.value.detail == "get_total_pulls"

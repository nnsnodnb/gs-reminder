import urllib.parse
from dataclasses import dataclass, field
from typing import Any

import requests
from requests.exceptions import HTTPError

from ..error import GitHubException
from .models.pull_request import PullRequest

GITHUB_API_BASE_URL = "https://api.github.com"


@dataclass(frozen=True)
class Client:
    github_token: str = field(repr=False, compare=False)

    def get_pulls(self, repo: str, limit: int) -> list[PullRequest]:
        api_url = f"{GITHUB_API_BASE_URL}/repos/{repo}/pulls"
        params: dict[str, Any] = {
            "state": "open",
            "sort": "created",
            "per_page": 25,
            "page": 1,
        }
        headers = {
            "Authorization": f"bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        pulls: list[PullRequest] = []
        while True:
            res = requests.get(url=api_url, params=params, headers=headers)
            res_json = res.json()
            try:
                res.raise_for_status()
            except HTTPError as e:
                raise GitHubException(status_code=e.response.status_code, response=res_json, detail="get_pulls") from e
            if not res_json:
                break

            # filter not draft pull requests
            items = (
                pull for item in res_json if not (pull := PullRequest(**item)).draft
            )
            pulls += items

            if len(pulls) >= limit:
                pulls = pulls[:limit]
                break

            value = params.get("page", 1)
            params["page"] = value + 1

        return pulls

    def get_total_pulls(self, repo: str) -> int:
        api_url = (
            f"{GITHUB_API_BASE_URL}/search/issues?q={urllib.parse.quote(f'type:pr repo:{repo} state:open')}&per_page=1"
        )
        headers = {
            "Authorization": f"bearer {self.github_token}",
            "Accept": "application/vnd.github.v3.text-match+json",
        }
        res = requests.get(url=api_url, headers=headers)
        res_json = res.json()
        try:
            res.raise_for_status()
        except HTTPError as e:
            raise GitHubException(
                status_code=e.response.status_code, response=res_json, detail="get_total_pulls"
            ) from e
        total_count = res_json["total_count"]

        return total_count

from typing import List

import requests

from .models.pull_request import PullRequest

GITHUB_API_BASE_URL = "https://api.github.com"


class Client:
    _github_token: str

    def __init__(self, token: str) -> None:
        self._github_token = token

    def get_pulls(self, repo: str) -> List[PullRequest]:
        api_url = f"{GITHUB_API_BASE_URL}/repos/{repo}/pulls"
        params = {"state": "open", "sort": "created", "per_page": 30, "page": 1}
        headers = {
            "Authorization": f"bearer {self._github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        prs = []
        while True:
            res = requests.get(url=api_url, params=params, headers=headers)
            res_json = res.json()
            if not res_json:
                break
            items = map(lambda item: PullRequest(**item), res_json)
            prs += items
            params["page"] += 1

        return prs

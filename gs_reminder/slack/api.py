import json
import os
from dataclasses import dataclass, field
from typing import Any

import requests
from requests.exceptions import HTTPError

from ..bridge import BridgeUsername
from ..error import SlackException
from ..github.models.pull_request import PullRequest
from ..github.models.user import User


@dataclass(frozen=True)
class Client:
    usernames: list[BridgeUsername]
    icon: bool
    exclude_users: list[str]
    _webhook_url: str = field(init=False, default_factory=lambda: os.environ["SLACK_URL"])

    def _convert_github_to_slack(self, user: User) -> str:
        for username in self.usernames:
            if username.github == user.login:
                return username.slack
        else:
            return user.login

    def _get_section(self, pull: PullRequest) -> list[dict[str, Any]]:
        # title section
        title_section: dict[str, Any] = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"[#{pull.number}] <{pull.html_url}|{pull.title}> (_{pull.user.login}_)",
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Review",
                },
                "url": pull.html_url,
            },
        }

        # reviewer section
        reviewer_section: dict[str, Any] = {"type": "context", "elements": []}
        requested_reviewers = list(filter(lambda obj: obj.login not in self.exclude_users, pull.requested_reviewers))
        if requested_reviewers:
            reviewer_section["elements"] += [
                {
                    "type": "plain_text",
                    "text": "Waiting on",
                },
            ]
            if self.icon:
                for reviewer in requested_reviewers:
                    reviewer_section["elements"] += [
                        {
                            "type": "image",
                            "image_url": reviewer.avatar_url,
                            "alt_text": reviewer.login,
                        },
                        {
                            "type": "mrkdwn",
                            "text": self._convert_github_to_slack(user=reviewer),
                        },
                    ]
            else:
                reviewer_section["elements"] += [
                    {
                        "type": "mrkdwn",
                        "text": " ".join(map(self._convert_github_to_slack, requested_reviewers)),
                    }
                ]
        else:
            reviewer_section["elements"] += [{"type": "plain_text", "text": "Waiting review by anyone."}]

        return [
            title_section,
            reviewer_section,
        ]

    def _build_block(self, repo: str, pulls: list[PullRequest], total_pulls: int) -> list[dict[str, Any]]:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Pending review on _<https://github.com/{repo}|{repo}>_*",
                },
            },
        ]

        for section in (self._get_section(pull) for pull in pulls):
            blocks += section

        if len(pulls) < total_pulls:
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Number of remaining: *{total_pulls - len(pulls)}*",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Watch",
                        },
                        "url": f"https://github.com/{repo}/pulls",
                    },
                },
            ]

        blocks += [
            {
                "type": "divider",
            },
        ]

        return blocks

    def post(self, repo: str, pulls: list[PullRequest], total_pulls: int) -> None:
        if not pulls:
            return

        payload: dict[str, Any] = {
            "text": f"Waiting your review on {repo}.",
            "blocks": self._build_block(repo=repo, pulls=pulls, total_pulls=total_pulls),
        }

        res = requests.post(url=self._webhook_url, data=json.dumps(payload))
        try:
            res.raise_for_status()
        except HTTPError as e:
            raise SlackException(status_code=res.status_code, content=res.content.decode("utf-8")) from e

from typing import List, Optional

from .user import User


class PullRequest(object):
    pr_id: int
    node_id: str
    html_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: User
    assignees: List[User]
    requested_reviewers: List[User]
    draft: Optional[bool]

    def __init__(self, **kwargs) -> None:
        self.pr_id = kwargs["id"]
        self.node_id = kwargs["node_id"]
        self.html_url = kwargs["html_url"]
        self.number = kwargs["number"]
        self.state = kwargs["state"]
        self.locked = kwargs["locked"]
        self.title = kwargs["title"]
        self.user = User(**kwargs["user"])
        self.assignees = list(map(lambda item: User(**item), kwargs.get("assignees", [])))
        self.requested_reviewers = list(map(lambda item: User(**item), kwargs["requested_reviewers"]))
        self.draft = kwargs["draft"]

    def __str__(self) -> str:
        title = f"Pull Request [#{self.number}] {self.title} from {str(self.user)}"
        if self.draft:
            title += "in draft"
        return title

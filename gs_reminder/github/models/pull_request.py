from typing import Annotated, List, Optional

from pydantic import BaseModel, Field

from .user import User


class PullRequest(BaseModel):
    pr_id: int = Field(alias="id")
    node_id: str
    html_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: User
    assignees: Annotated[List[User], Field(default_factory=lambda: list)]
    requested_reviewers: Annotated[List[User], Field(default_factory=lambda: list)]
    draft: Optional[bool]

    def __str__(self) -> str:
        title = f"Pull Request [#{self.number}] {self.title} from {str(self.user)}"
        if self.draft:
            title += "in draft"
        return title

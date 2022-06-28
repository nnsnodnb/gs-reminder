from typing import Any, Dict


class _AbstractException(Exception):
    status_code: int
    response: Dict[Any, Any]

    def __init__(self, status_code: int, response: Dict[Any, Any]) -> None:
        self.status_code = status_code
        self.response = response


class GitHubException(_AbstractException):
    detail: str

    def __init__(self, status_code: int, response: Dict[Any, Any], detail: str) -> None:
        self.status_code = status_code
        self.response = response
        self.detail = detail
        super().__init__(status_code=status_code, response=response)


class SlackException(_AbstractException):
    pass

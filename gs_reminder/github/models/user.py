class User(object):
    login: str
    user_id: int
    user_type: str
    avatar_url: str

    def __init__(self, **kwargs) -> None:
        self.login = kwargs["login"]
        self.user_id = kwargs["id"]
        self.user_type = kwargs["type"]
        self.avatar_url = kwargs["avatar_url"]

    def __str__(self) -> str:
        user = f"@{self.login}"
        if self.user_type != "User":
            user += f" [{self.user_type}]"
        return user

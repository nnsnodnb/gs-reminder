class BridgeUsername:
    github: str
    slack: str

    def __init__(self, **kwargs) -> None:
        self.github = kwargs["github"]
        self.slack = kwargs["slack"]
        if not self.slack.startswith("@"):
            self.slack = f"@{self.slack}"

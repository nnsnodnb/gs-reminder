from dataclasses import dataclass


@dataclass
class BridgeUsername:
    github: str
    slack: str

    def __post_init__(self) -> None:
        if not self.slack.startswith("@"):
            self.slack = f"@{self.slack}"

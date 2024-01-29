from pydantic import BaseModel, Field


class User(BaseModel):
    login: str
    user_id: int = Field(alias="id")
    user_type: str = Field(alias="type")
    avatar_url: str

    def __str__(self) -> str:
        user = f"@{self.login}"
        if self.user_type != "User":
            user += f" [{self.user_type}]"
        return user

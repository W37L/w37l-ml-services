from pydantic import BaseModel
from typing import Union

class UserRelations(BaseModel):
    userid: str
    blockedUsers: list[str]
    following: list[str]
    followers: list[str]
    higthlightedTweetIds: list[str]
    likedTweetIds: list[str]
    mutedUsers: list[str]
    reportedUsers: list[str]
    reTweetedTweetIds: list[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class Post(BaseModel):
    content: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class Response(BaseModel):
    """
    Represents a generic API response containing information about success and a message.

    The `message` attribute can be either:

    - A single string: This is a common case for simple success/error messages.
    - A list of lists of strings: The specific meaning and structure of this format
      depend on the API implementation. Consult the API documentation for details.
    """
    
    success: bool
    message: Union[str, list[list[str]]]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
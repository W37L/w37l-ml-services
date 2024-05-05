from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    userid: str
    name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class Post(BaseModel):
    postid: str
    title: str
    userid: str
    content: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class Response(BaseModel):
    success: bool
    message: Union[str, list[list[str]]]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
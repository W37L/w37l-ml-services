from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    def __init__(self, userid: str, name: str):
        self.userid = userid
        self.name = name

    @classmethod
    def create(cls, userid: str, name: str):
        return cls(userid, name)

class Post:
    def __init__(self, postid: str, title: str, userid: str, content: str):
        self.postid = postid
        self.title = title
        self.userid = userid
        self.content = content

    @classmethod
    def create(cls, postid: str, title: str, userid: str, content: str):
        return cls(postid, title, userid, content)
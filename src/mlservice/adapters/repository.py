from abc import ABC

from mlservice.models.model import Post
from mlservice.models.model import User


class IMachineLearningRepository(ABC):
    def get_user(self, userid: str) -> User:
        ...

    def add_user(self, user: User) -> None:
        ...

    def get_posts(self, userid: str) -> list[Post]:
        ...

    def get_last_posts(self) -> list[str]:
        ...
    
    def add_post(self, post: Post) -> None:
        ...
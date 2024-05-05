from abc import ABC

from src.mlservice.model.model import *


class IMachineLearningRepository(ABC):
    def get_user(self, userid: str) -> User:
        ...

    def get_following_users(self, userid: str) -> list[User]:
        ...

    def get_posts(self, userid: str) -> list[Post]:
        ...

    def get_last_posts(self) -> list[str]:
        ...
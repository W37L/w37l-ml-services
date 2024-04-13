from abc import ABC

from src.domain.model import User
from src.domain.model import Post


class IMachineLearningService(ABC):
    def check_profanity(self, text: str) -> bool:
        ...

    def get_trending_topics(self) -> list[str]:
        ...

    def get_recomendation_user(self, user: User) -> list[User]:
        ...
    
    def get_recomendation_post(self, user: User) -> list[Post]:
        ...
from abc import ABC, abstractmethod

from src.mlservice.model.model import *


class IMachineLearningService(ABC):
    @abstractmethod
    def check_profanity(self, text: str) -> Response:
        ...

    @abstractmethod
    def get_hashtag(self, text: str) -> Response:
        ...

    @abstractmethod
    def get_trending_topics(self) -> Response:
        ...

    @abstractmethod
    def get_recommendation_user(self, user: str) -> Response:
        ...

    @abstractmethod
    def get_recommendation_post(self, user: str) -> Response:
        ...
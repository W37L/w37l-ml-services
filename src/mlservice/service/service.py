from abc import ABC, abstractmethod

from src.mlservice.model.model import *


class IMachineLearningService(ABC):
    @abstractmethod
    def check_profanity(self, text: str) -> Response:
        """
        Checks if the provided text contains profanity using a pre-trained model.

        Args:
            text: The text to be checked for profanity.

        Returns:
            A Response object indicating success (with or without profanity) and message.
        """
        ...

    @abstractmethod
    def get_hashtag(self, text: str) -> Response:
        """
        Retrieves a str with the hashtag based on the post.

        Returns:
            A Response object indicating success and message containing the hashtag.
        """
        ...

    @abstractmethod
    def get_trending_topics(self) -> Response:
        """
        Retrieves a list of trending topics based on the latest posts, using
        topic modeling techniques.

        Returns:
            A list of Response objects representing the trending topics.
        """
        ...

    @abstractmethod
    def get_recommendation_user(self, user: User) -> list[User]:
        """
        Recommends users to follow based on the provided user's profile and interactions.

        Args:
            user: The user for whom recommendations are generated.

        Returns:
            A list of User objects for recommended users.
        """
        pass

    @abstractmethod
    def get_recommendation_post(self, user: User) -> list[Post]:
        """
        Recommends posts to the provided user based on their interests and interactions.

        Args:
            user: The user for whom recommendations are generated.

        Returns:
            A list of Post objects for recommended posts.
        """
        pass
from abc import ABC

from src.mlservice.model.model import *  # Assuming this imports User and Post classes


class IMachineLearningRepository(ABC):
    """
    Interface defining methods for interacting with a machine learning model repository.

    This interface provides methods for retrieving user information, their following users,
    their posts, and potentially the latest posts from the repository.

    Concrete implementations of this interface will handle the specific storage mechanisms 
    and retrieval logic for the machine learning model data.
    """

    def get_user_relations(self, userid: str) -> list[UserRelations]:
        ...
    
    def get_last_posts(self) -> list[Post]:
        ...
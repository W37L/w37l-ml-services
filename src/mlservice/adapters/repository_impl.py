import pandas as pd
import logging
import requests
from dataclasses import dataclass

from src.mlservice.model.model import *
from src.mlservice.adapters.repository import IMachineLearningRepository

class RepositoryEntryNotFound(Exception):
    """Raised when a requested user or post entry is not found."""
    pass

@dataclass
class MachineLearningRepository(IMachineLearningRepository):
    storage_dir: str

    def get_user_relations(self, userid: str) -> list[UserRelations]:
        """
        Fetches user relations data for a list of user IDs and returns a list of UserRelations objects.

        Args:
            user_ids (list[str]): A list of user IDs to fetch data for.

        Returns:
            list[UserRelations]: A list of UserRelations objects containing user relation data.
        """

        # Define the API endpoint URL
        api_url = f"/api/users/{userid}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            user_data = data.get("User")  # Handle potential missing "User" key

            if not user_data:
                raise RepositoryEntryNotFound(f"User with ID {userid} not found")

            # Extract data and map to corresponding attributes
            user_relations = UserRelations(
                userid=user_data.get("userId"),
                blockedUsers=user_data.get("blockedUsers", []),
                following=user_data.get("following", []),
                followers=user_data.get("followers", []),
                higthlightedTweetIds=user_data.get("higthlightedTweetIds", []),
                likedTweetIds=user_data.get("likedTweetIds", []),
                mutedUsers=user_data.get("mutedUsers", []),
                reportedUsers=user_data.get("reportedUsers", []),
                reTweetedTweetIds=user_data.get("reTweetedTweetIds", []),
            )
            
            # Return a list containing the user relations
            return [user_relations]

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching user from API: {e}")
            raise RepositoryEntryNotFound(f"User with ID {userid} not found")
        
        except Exception as e:  # Catch any other unexpected exceptions
            logging.error(f"Unexpected error: {e}")
            raise RepositoryEntryNotFound(f"User with ID {userid} not found")
    
    def get_last_posts(self) -> list[Post]:
        """
        Fetches a list of the latest posts from the API and returns them as Post objects.

        Returns:
            list[Post]: A list of Post objects containing the latest posts.
        """

        # Define the API endpoint URL
        api_url = "/api/getPosts"

        try:
            response = requests.get(self.storage_dir + api_url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()  # Assuming the response is JSON
            post_data_list = data.get("Content", [])

            # Convert each data entry to a Post object
            posts = [Post.from_dict(post_data) for post_data in post_data_list]

            return posts

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching posts from API: {e}")
            raise RepositoryEntryNotFound("Error fetching posts from API")
        
        except Exception as e:  # Catch any other unexpected exceptions
            logging.error(f"Unexpected error: {e}")
            raise RepositoryEntryNotFound("Error fetching posts from API")

@dataclass
class MockMachineLearningRepository(IMachineLearningRepository):
    """Mock implementation of the MachineLearningRepository interface, used for testing purposes."""

    def get_user_relations() -> list[UserRelations]:
        try:
            df = pd.read_excel('training_models/test2.xlsx')

            user_relations_list = []
            for index, row in df.iterrows():
                user_relations = UserRelations(
                    userid=row.get("userid"),
                    blockedUsers=row.get("blockedUsers", []),
                    following=row.get("following", []),
                    followers=row.get("followers", []),
                    higthlightedTweetIds=row.get("higthlightedTweetIds", []),
                    likedTweetIds=row.get("likedTweetIds", []),
                    mutedUsers=row.get("mutedUsers", []),
                    reportedUsers=row.get("reportedUsers", []),
                    reTweetedTweetIds=row.get("reTweetedTweetIds", []),
                )
                user_relations_list.append(user_relations)

            return user_relations_list

        except Exception as e:
            logging.error(f"Error loading user data from Excel file: {e}")
            raise NotImplementedError("User retrieval is not implemented in the mock repository")

    def get_last_posts(self) -> list[str]:
        try:
            df = pd.read_excel('training_models/test1.xlsx')

            # Assuming 'Text' column contains post content
            post_data_list = df['Text'].tolist()

            # Create a list of Post objects using the class method
            posts = [Post.from_dict({'content': content}) for content in post_data_list]

            return posts
        except Exception as e:
            logging.error(f"Error loading post data from Excel file: {e}")
            raise RepositoryEntryNotFound("Error loading post data from Excel file")
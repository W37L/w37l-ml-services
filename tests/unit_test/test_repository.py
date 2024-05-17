import unittest
from unittest.mock import patch, MagicMock

from src.mlservice.adapters.repository import (
    MachineLearningRepository,
    MockMachineLearningRepository,
    RepositoryEntryNotFound,
)
import requests


class TestMachineLearningRepository(unittest.TestCase):

    @patch('requests.get')  # Patch the requests.get function for mocking API calls
    def test_get_user_relations_success(self, mock_get):
        """
        Test successful retrieval of user relations from the API.
        """
        user_id = "test_user_123"
        expected_data = {
            "userId": "user123",
            "blockedUsers": ["user456", "user789"],
            "following": ["user001", "user999"],
            "followers": ["user333", "user555"],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = {"User": expected_data}
        mock_get.return_value = mock_response

        repository = MachineLearningRepository()
        user_relations = repository.get_user_relations(user_id)

        self.assertEqual(user_relations.userid, expected_data["userId"])
        self.assertEqual(user_relations.blockedUsers, expected_data["blockedUsers"])
        self.assertEqual(user_relations.following, expected_data["following"])

    @patch('requests.get')
    def test_get_user_relations_not_found(self, mock_get):
        """
        Test handling of user not found in the API response.
        """
        user_id = "unknown_user"
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # User key not present
        mock_get.return_value = mock_response

        repository = MachineLearningRepository()
        with self.assertRaises(RepositoryEntryNotFound) as context:
            repository.get_user_relations(user_id)

        self.assertEqual(str(context.exception), f"User with ID {user_id} not found")

    @patch('requests.get')
    def test_get_user_relations_api_error(self, mock_get):
        """
        Test handling of API request errors.
        """
        user_id = "test_user_123"
        mock_get.side_effect = requests.exceptions.RequestException("API connection error")

        repository = MachineLearningRepository()
        with self.assertRaises(RepositoryEntryNotFound) as context:
            repository.get_user_relations(user_id)

        self.assertEqual(str(context.exception), f"User with ID {user_id} not found")

    @patch('pd.read_excel')  # Patch pandas.read_excel for mocking data loading
    def test_get_last_posts_success(self, mock_read_excel):
        """
        Test successful retrieval of last posts from the mock repository.
        """
        expected_post_data = [
            {"content": "This is the first post"},
            {"content": "This is the second post"},
        ]
        mock_dataframe = MagicMock()
        mock_dataframe.__getitem__.side_effect = lambda col: expected_post_data if col == 'Text' else []  # Simulate getting content column
        mock_read_excel.return_value = mock_dataframe

        repository = MockMachineLearningRepository()  # Use the MockMachineLearningRepository
        posts = repository.get_last_posts()

        self.assertEqual(len(posts), len(expected_post_data))
        for i, post in enumerate(posts):
            self.assertEqual(post.content, expected_post_data[i]["content"])

    @patch('pd.read_excel')
    def test_get_last_posts_error(self, mock_read_excel):
        """
        Test handling of errors during data loading from the mock repository.
        """
        mock_read_excel.side_effect = Exception("Error reading data from Excel file")

        repository = MockMachineLearningRepository()  # Use the MockMachineLearningRepository
        with self.assertRaises(RepositoryEntryNotFound) as context:
            repository.get_last_posts()

        self.assertEqual(str(context.exception), "Error fetching posts from API")  # Consistent error message

if __name__ == '__main__':
    unittest.main()

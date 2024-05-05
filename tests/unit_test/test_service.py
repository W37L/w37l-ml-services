import unittest
from unittest.mock import patch, MagicMock

from src.mlservice.service import MachineLearningService
from src.mlservice.model.model import User, Post
from src.mlservice.adapters.repository import IMachineLearningRepository


class MachineLearningServiceTest(unittest.TestCase):

    @patch('src.mlservice.service.joblib.load')
    def test_check_profanity_success(self, mock_load):
        # Mock successful loading of model and vectorizer
        mock_load.side_effect = [MagicMock(), MagicMock()]
        service = MachineLearningService(MagicMock())  # Mock repository

        # Test content with profanity
        profanity_content = "This is some offensive content."
        response = service.check_profanity(profanity_content)

        self.assertTrue(response.success)
        self.assertEqual(response.error, "Profanity detected")

    @patch('src.mlservice.service.joblib.load')
    def test_check_profanity_no_profanity(self, mock_load):
        # Mock successful loading of model and vectorizer
        mock_load.side_effect = [MagicMock(), MagicMock()]
        service = MachineLearningService(MagicMock())  # Mock repository

        # Test content without profanity
        clean_content = "This is a harmless message."
        response = service.check_profanity(clean_content)

        self.assertTrue(response.success)
        self.assertEqual(response.error, "No profanity detected")

    @patch('src.mlservice.service.joblib.load')
    def test_check_profanity_model_not_found(self, mock_load):
        # Mock model load to raise FileNotFoundError
        mock_load.side_effect = FileNotFoundError("Model not found")
        service = MachineLearningService(MagicMock())  # Mock repository

        response = service.check_profanity("Some content")

        self.assertFalse(response.success)
        self.assertEqual(response.error, "Profanity detection model or vectorizer not found.")

    def test_get_trending_topics(self):
        # Placeholder test - Modify as you implement the logic
        mock_repository = MagicMock()
        mock_repository.get_last_posts.return_value = []  # Empty list
        service = MachineLearningService(mock_repository)

        topics = service.get_trending_topics()

        self.assertEqual(topics, [])  # Empty list returned

    def test_get_recommendation_user(self):
        # Placeholder test - Modify as you implement the logic
        mock_repository = MagicMock()
        service = MachineLearningService(mock_repository)

        # Provide a User object for the test
        user = User("user123", "John Doe")
        recommendations = service.get_recommendation_user(user)

        self.assertEqual(recommendations, [])  # Empty list returned

    def test_get_recommendation_post(self):
        # Placeholder test - Modify as you implement the logic
        mock_repository = MagicMock()
        service = MachineLearningService(mock_repository)

        # Provide a User object for the test
        user = User("user123", "John Doe")
        recommendations = service.get_recommendation_post(user)

        self.assertEqual(recommendations, [])  # Empty list returned


if __name__ == '__main__':
    unittest.main()
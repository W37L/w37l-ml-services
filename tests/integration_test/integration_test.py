import json
import unittest
from unittest.mock import patch
from src.mlservice.service.service import IMachineLearningService  # Assuming the service interface
from requests import post, get

BASE_URL = "http://localhost:8000"


class TestMLServiceAPI(unittest.TestCase):

    def test_check_profanity_success(self):
        url = f"{BASE_URL}/MLService/checkProfanity"
        data = {"text": "This is a normal sentence."}
        response = post(url, json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertIn("success", response_data)  # Check for presence of success key

    def test_check_profanity_failure(self):
        url = f"{BASE_URL}/MLService/checkProfanity"
        data = {"text": "This contains a swear word."}
        response = post(url, json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertIn("success", response_data)  # Check for presence of success key

    @patch('src.mlservice.service.service.IMachineLearningService.get_trending_topics')
    def test_get_trending_topics_success(self, mock_get_trending_topics):
        url = f"{BASE_URL}/MLService/getTrendingTopics"
        mocked_data = [
            {"id": 1, "title": "Topic 1"},
            {"id": 2, "title": "Topic 2"},
        ]
        mock_get_trending_topics.return_value = mocked_data
        response = get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data, mocked_data)

    @patch('src.mlservice.service.service.IMachineLearningService.get_trending_topics')
    def test_get_trending_topics_error(self, mock_get_trending_topics):
        url = f"{BASE_URL}/MLService/getTrendingTopics"
        mock_get_trending_topics.side_effect = Exception("Mocked error during trending topic retrieval")
        response = get(url)
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.text)
        self.assertIn("error", response_data)  # Check for presence of error key

    def test_recommendation_user_placeholder(self):
        user_id = "test_user"
        url = f"{BASE_URL}/MLService/recomendationUser"
        response = get(url, params={"userId": user_id})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertIn("success", response_data)  # Check for presence of success key
        self.assertTrue(response_data["success"])  # Assert successful recommendation

        self.assertIn("recommendations", response_data)
        recommendations = response_data["recommendations"]
        self.assertIsInstance(recommendations, list)  # Assert recommendations is a list
        self.assertGreaterEqual(len(recommendations), 0)  # Assert at least one recommendation


    def test_recommendation_post_placeholder(self):
        user_id = "test_user"
        url = f"{BASE_URL}/MLService/recomendationPost"
        response = get(url, params={"userId": user_id})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertIn("success", response_data)  # Check for presence of success key
        self.assertTrue(response_data["success"])  # Assert successful recommendation

        self.assertIn("recommendations", response_data)
        recommendations = response_data["recommendations"]
        self.assertIsInstance(recommendations, list)  # Assert recommendations is a list
        self.assertGreaterEqual(len(recommendations), 0)  # Assert at least one recommendation

if __name__ == "__main__":
    unittest.main()
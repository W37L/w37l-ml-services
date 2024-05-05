import json
import unittest
from unittest.mock import patch
from src.mlservice.service.service import IMachineLearningService


from requests import post, get

# Replace with the base URL of your FastAPI application
BASE_URL = "http://localhost:8000"  # Adjust port if needed

class TestMLServiceAPI(unittest.TestCase):

    def test_check_profanity_success(self):
        url = f"{BASE_URL}/MLService/checkProfanity"
        data = {"text": "This is a normal sentence."}
        response = post(url, json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data["success"], True)

    def test_check_profanity_failure(self):
        url = f"{BASE_URL}/MLService/checkProfanity"
        data = {"text": "This contains a swear word."}
        response = post(url, json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data["success"], False)

    def test_get_trending_topics_success(self):
        url = f"{BASE_URL}/MLService/getTrendingTopics"
        mocked_data = [
            {"id": 1, "title": "Topic 1"},
            {"id": 2, "title": "Topic 2"},
        ]
        response = get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.text)
        self.assertEqual(response_data, mocked_data)

    def test_get_trending_topics_error(self):
        url = f"{BASE_URL}/MLService/getTrendingTopics"
        def mock_get_trending_topics():
            raise Exception("Mocked error during trending topic retrieval")

        with patch.object(IMachineLearningService, "get_trending_topics", mock_get_trending_topics):
            response = get(url)
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.text)
        self.assertIn("error", response_data)

if __name__ == "__main__":
    unittest.main()
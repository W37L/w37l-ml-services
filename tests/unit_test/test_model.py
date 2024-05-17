import unittest
from pydantic import ValidationError
from src.mlservice.model.model import UserRelations, Post, Response

class TestUserRelations(unittest.TestCase):

    def test_valid_data(self):
        """
        Test UserRelations model with valid data.
        """
        data = {
            "userid": "user123",
            "blockedUsers": ["user456", "user789"],
            "following": ["user001", "user999"],
            "followers": ["user333", "user555"],
            "higthlightedTweetIds": ["tweet1", "tweet2"],
            "likedTweetIds": ["tweet3", "tweet4"],
            "mutedUsers": ["userABC", "userXYZ"],
            "reportedUsers": ["userMNO", "userPQR"],
            "reTweetedTweetIds": ["tweet5", "tweet6"],
        }
        user_relations = UserRelations(**data)

        self.assertEqual(user_relations.userid, data["userid"])
        self.assertEqual(user_relations.blockedUsers, data["blockedUsers"])
        self.assertEqual(user_relations.following, data["following"])
        # ... (similar assertions for other attributes)

    def test_missing_data(self):
        """
        Test UserRelations model with missing data.
        """
        data = {"userid": "user123"}
        with self.assertRaises(ValidationError):
            UserRelations(**data)

        data = {}
        with self.assertRaises(ValidationError):
            UserRelations(**data)

    def test_invalid_data_type(self):
        """
        Test UserRelations model with invalid data types.
        """
        data = {
            "userid": 123,  # Integer instead of string
            "blockedUsers": "invalid_list",  # String instead of list
        }
        with self.assertRaises(ValidationError):
            UserRelations(**data)


if __name__ == "__main__":
    unittest.main()

class TestPost(unittest.TestCase):

    def test_valid_data(self):
        """
        Test Post model with valid data.
        """
        data = {"content": "This is a sample post."}
        post = Post(**data)

        self.assertEqual(post.content, data["content"])

    def test_missing_data(self):
        """
        Test Post model with missing data.
        """
        data = {}
        with self.assertRaises(ValidationError):
            Post(**data)


if __name__ == "__main__":
    unittest.main()

class TestResponse(unittest.TestCase):

    def test_valid_data_single_string(self):
        """
        Test Response model with valid data (single string message).
        """
        data = {"success": True, "message": "Operation successful."}
        response = Response(**data)

        self.assertEqual(response.success, data["success"])
        self.assertEqual(response.message, data["message"])

    def test_valid_data_list_message(self):
        """
        Test Response model with valid data (list of lists message).
        """
        data = {
            "success": False,
            "message": [
                ["Error code 1", "Error message 1"],
                ["Error code 2", "Error message 2"],
            ],
        }
        response = Response(**data)

        self.assertEqual(response.success, data["success"])
        self.assertEqual(response.message, data["message"])

    def test_invalid_data(self):
        """
        Test Response model with invalid data.
        """
        data = {"success": True}  # Missing message field
        with self.assertRaises(ValidationError):
            Response(**data)


if __name__ == "__main__":
    unittest.main()
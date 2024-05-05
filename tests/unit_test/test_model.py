import unittest
from src.mlservice.model.model import User
from src.mlservice.model.model import Post
from src.mlservice.model.model import Response


class UserTest(unittest.TestCase):

    def test_user_creation(self):
        user = User.create("user123", "John Doe")

        self.assertEqual(user.userid, "user123")
        self.assertEqual(user.name, "John Doe")

    def test_user_creation_empty_userid(self):
        with self.assertRaises(ValueError):
            User.create("", "John Doe")

    def test_user_creation_empty_name(self):
        with self.assertRaises(ValueError):
            User.create("user123", "")


if __name__ == '__main__':
    unittest.main()



class PostTest(unittest.TestCase):

    def test_post_creation(self):
        post = Post.create("post1", "Sample Title", "user_abc", "This is the post content.")

        self.assertEqual(post.postid, "post1")
        self.assertEqual(post.title, "Sample Title")
        self.assertEqual(post.userid, "user_abc")
        self.assertEqual(post.content, "This is the post content.")

    def test_post_creation_empty_postid(self):
        with self.assertRaises(ValueError):
            Post.create("", "Sample Title", "user_abc", "This is the post content.")

    def test_post_creation_empty_title(self):
        with self.assertRaises(ValueError):
            Post.create("post1", "", "user_abc", "This is the post content.")

    def test_post_creation_empty_userid(self):
        with self.assertRaises(ValueError):
            Post.create("post1", "Sample Title", "", "This is the post content.")

    def test_post_creation_empty_content(self):
        with self.assertRaises(ValueError):
            Post.create("post1", "Sample Title", "user_abc", "")



class ResponseTest(unittest.TestCase):

    def test_response_creation_success(self):
        response = Response.create(True)

        self.assertTrue(response.success)
        self.assertIsNone(response.error)

    def test_response_creation_error(self):
        response = Response.create(False, "An error occurred.")

        self.assertFalse(response.success)
        self.assertEqual(response.error, "An error occurred.")


if __name__ == '__main__':
    unittest.main()
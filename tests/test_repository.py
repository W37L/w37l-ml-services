from tempfile import TemporaryDirectory

import pytest as pytest

from src.container import ApplicationContainer
from src.domain.model import User
from src.domain.model import Post
from src.adapters.repository_impl import (
    IMachineLearningRepository,
)


@pytest.fixture()
def repository():
    with TemporaryDirectory() as tmp_dir:
        container = ApplicationContainer()

        container.configuration.storage_dir.from_value(tmp_dir)
        yield container.todo_entry_repository()


def test_add_and_get_user(repository: IMachineLearningRepository):
    entry = User.create("test01", "John Doe")
    repository.add_user(entry)
    assert entry == repository.get_user(entry.userid)

def test_add_and_get_posts(repository: IMachineLearningRepository):
    entry = User.create("user01", "John Doe")
    repository.add_user(entry)
    post = Post.create("post01", "Hello, World", entry.userid, "Lorem Ipsum Dolor Sit Amet")
    repository.add_post(post)
    assert [post] == repository.get_posts(entry.userid)

from unittest.mock import Mock

import pytest

from bookshelf.repositories.protocols import AuthorRepository


@pytest.fixture
def author_repo_mock():
    return Mock(spec=AuthorRepository)

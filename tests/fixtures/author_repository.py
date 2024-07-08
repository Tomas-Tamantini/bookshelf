from unittest.mock import Mock

import pytest

from bookshelf.repositories.protocols import AuthorRepository


@pytest.fixture
def author_repo_mock(author):
    repo = Mock(spec=AuthorRepository)
    repo.add.return_value = author
    return repo
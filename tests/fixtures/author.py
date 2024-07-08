import pytest

from bookshelf.domain.author import Author


@pytest.fixture
def author():
    return Author(id=1, name="Author Name")

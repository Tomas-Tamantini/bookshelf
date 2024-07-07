from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.in_memory import InMemoryAuthorRepository


def test_adding_author_in_memory_increments_id():
    repository = InMemoryAuthorRepository()
    auth_1 = repository.add(AuthorCore(name="Author 1"))
    assert auth_1 == Author(id=1, name="Author 1")
    auth_2 = repository.add(AuthorCore(name="Author 2"))
    assert auth_2 == Author(id=2, name="Author 2")

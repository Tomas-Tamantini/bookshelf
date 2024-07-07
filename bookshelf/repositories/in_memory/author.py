from bookshelf.domain.author import Author, AuthorCore


class InMemoryAuthorRepository:
    def __init__(self):
        self._authors = []

    def add(self, author: AuthorCore) -> Author:
        author = Author(id=len(self._authors) + 1, **author.model_dump())
        self._authors.append(author)
        return author

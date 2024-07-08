from bookshelf.domain.author import Author, AuthorCore


class InMemoryAuthorRepository:
    def __init__(self):
        self._authors = []

    def add(self, author: AuthorCore) -> Author:
        author = Author(id=len(self._authors) + 1, **author.model_dump())
        self._authors.append(author)
        return author

    def name_exists(self, name: str) -> bool:
        return any(author.name == name for author in self._authors)

    def id_exists(self, author_id: int) -> bool:
        return any(author.id == author_id for author in self._authors)

    def delete(self, author_id: int) -> None:
        self._authors = [author for author in self._authors if author.id != author_id]

    def update(self, author_id: int, updated: AuthorCore) -> Author:
        updated = Author(id=author_id, **updated.model_dump())
        self._authors = [
            updated if author.id == author_id else author for author in self._authors
        ]
        return updated

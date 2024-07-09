from bookshelf.domain.book import Book, BookCore


class InMemoryBookRepository:
    def add(self, book: BookCore) -> Book:
        raise NotImplementedError()

    def title_exists(self, title: str) -> bool:
        raise NotImplementedError()

from bookshelf.domain.book import Book, BookCore


class InMemoryBookRepository:
    def add(self, book: BookCore) -> Book:
        raise NotImplementedError()

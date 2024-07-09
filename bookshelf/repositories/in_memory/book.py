from bookshelf.domain.book import Book, BookCore


class InMemoryBookRepository:
    def __init__(self) -> None:
        self._books = []

    def add(self, book: BookCore) -> Book:
        book = Book(id=len(self._books) + 1, **book.model_dump())
        self._books.append(book)
        return book

    def title_exists(self, title: str) -> bool:
        return any(book.title == title for book in self._books)

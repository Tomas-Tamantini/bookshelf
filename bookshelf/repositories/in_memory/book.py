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

    def id_exists(self, book_id: int) -> bool:
        return any(book.id == book_id for book in self._books)

    def delete(self, book_id: int) -> None:
        self._books = [book for book in self._books if book.id != book_id]

    def update(self, book_id: int, book: BookCore) -> Book:
        raise NotImplementedError()

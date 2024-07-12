from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import GetBooksDBQueryParameters, GetBooksDBResponse
from bookshelf.repositories.exceptions import ConflictError


class InMemoryBookRepository:
    def __init__(self) -> None:
        self._books = []

    def add(self, element: BookCore) -> Book:
        if self._title_exists(element.title):
            raise ConflictError("title")
        book = Book(id=len(self._books) + 1, **element.model_dump())
        self._books.append(book)
        return book

    def _title_exists(self, title: str) -> bool:
        return any(book.title == title for book in self._books)

    def id_exists(self, element_id: int) -> bool:
        return any(book.id == element_id for book in self._books)

    def delete(self, element_id: int) -> None:
        self._books = [book for book in self._books if book.id != element_id]

    def _title_changed(self, book_id: int, book: BookCore) -> bool:
        old_book = self.get_by_id(book_id)
        return old_book.title != book.title

    def update(self, element_id: int, element: BookCore) -> Book:
        if self._title_changed(element_id, element) and self._title_exists(
            element.title
        ):
            raise ConflictError("title")
        updated = Book(id=element_id, **element.model_dump())
        self._books = [
            updated if book.id == element_id else book for book in self._books
        ]
        return updated

    def get_by_id(self, element_id: int) -> Book:
        return next((book for book in self._books if book.id == element_id), None)

    def get_filtered(
        self, query_parameters: GetBooksDBQueryParameters
    ) -> GetBooksDBResponse:
        filtered = [
            book for book in self._books if self._matches(book, query_parameters)
        ]
        start_idx = query_parameters.offset
        end_idx = start_idx + query_parameters.limit
        return GetBooksDBResponse(
            books=filtered[start_idx:end_idx], total=len(filtered)
        )

    def _matches(self, book: Book, query_parameters: GetBooksDBQueryParameters) -> bool:
        if (
            query_parameters.title is not None
            and query_parameters.title not in book.title
        ):
            return False
        if (
            query_parameters.author_id is not None
            and query_parameters.author_id != book.author_id
        ):
            return False
        if query_parameters.year is not None and query_parameters.year != book.year:
            return False
        return True

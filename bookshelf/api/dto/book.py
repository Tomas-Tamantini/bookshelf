from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.book import BookCore


class CreateBookRequest(BookCore):
    def sanitized(self) -> BookCore:
        return BookCore(
            title=sanitize_name(self.title),
            year=self.year,
            author_id=self.author_id,
        )

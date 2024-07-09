import pytest

from bookshelf.api.dto import PatchBookRequest
from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.book import Book, BookCore


@pytest.mark.parametrize(
    "dirty, clean",
    [
        ("Machado de Assis", "machado de assis"),
        (
            "O mundo assombrado pelos demônios",
            "o mundo assombrado pelos demônios",
        ),
    ],
)
def test_sanitizing_name_converts_to_lower_case(dirty, clean):
    assert sanitize_name(dirty) == clean


@pytest.mark.parametrize(
    "dirty, clean",
    [
        ("Manuel        Bandeira", "manuel bandeira"),
        ("Edgar Alan Poe         ", "edgar alan poe"),
        ("  breve  história  do tempo ", "breve história do tempo"),
    ],
)
def test_sanitizing_name_gets_rid_of_extra_spaces(dirty, clean):
    assert sanitize_name(dirty) == clean


def test_sanitizing_name_gets_rid_of_punctuation():
    assert (
        sanitize_name("Androides Sonham Com Ovelhas Elétricas?")
        == "androides sonham com ovelhas elétricas"
    )


def test_patch_book_requests_keeps_existing_values_for_not_informed_fields():
    existing_book = Book(id=1, title="Title", year=1999, author_id=1)
    patch = PatchBookRequest(title="new title", author_id=123)
    updated = patch.updated(existing_book)
    assert updated == BookCore(title="new title", year=1999, author_id=123)


def test_patch_book_requests_sanitizes_new_title():
    existing_book = Book(id=1, title="Title", year=1999, author_id=1)
    patch = PatchBookRequest(title="  new Title  ", year=2020)
    updated = patch.updated(existing_book)
    assert updated == BookCore(title="new title", year=2020, author_id=1)

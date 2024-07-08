from bookshelf.api.dto.sanitize import sanitize_name
import pytest


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

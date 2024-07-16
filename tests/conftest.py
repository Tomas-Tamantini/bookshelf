from tests.fixtures.authentication import mock_jwt_handler, mock_password_handler
from tests.fixtures.author import author
from tests.fixtures.author_repository import (
    get_authors_db_response,
    mock_author_repository,
)
from tests.fixtures.book import book, valid_book_request
from tests.fixtures.book_repository import get_books_db_response, mock_book_repository
from tests.fixtures.client import client, end_to_end_client
from tests.fixtures.user import user, user_core, valid_user_request
from tests.fixtures.user_repository import get_users_db_response, mock_user_repository

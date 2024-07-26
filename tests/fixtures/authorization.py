from unittest.mock import Mock

import pytest

from bookshelf.domain.authorization import Authorization


@pytest.fixture
def mock_update_user_authorization():
    authorization = Mock(spec=Authorization)
    authorization.has_permission.return_value = True
    return authorization


@pytest.fixture
def mock_delete_user_authorization():
    authorization = Mock(spec=Authorization)
    authorization.has_permission.return_value = True
    return authorization

import uuid
from urllib.parse import urlencode

import httpx
import pytest

from service.auth.hashing import hash_password
from service.models.users import Users


class TestLogin:
    def execute(self, api: httpx.Client, password: str = "qwerty123"):
        response = api.post(
            "/api/v1/auth/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(
                {
                    "email": "test@example.com",
                    "password": password,
                }
            ),
        )
        response.raise_for_status()
        return response

    def test_login_returns_jwt_pair(self, db_session, api):
        user = Users(id=uuid.uuid4(), username="test1", email="test@example.com", password_hash=hash_password("qwerty123"))
        db_session.add(user)
        db_session.commit()

        response = self.execute(api)
        assert response.status_code == 200

    def test_user_not_found_returns_403_error(self, api):
        with pytest.raises(httpx.HTTPStatusError, match="403 Forbidden"):
            self.execute(api)

    def test_wrong_password_returns_403_error(self, db_session, api):
        user = Users(id=uuid.uuid4(), username="test1", email="test@example.com", password_hash=hash_password("qwerty123"))
        db_session.add(user)
        db_session.commit()

        with pytest.raises(httpx.HTTPStatusError, match="403 Forbidden"):
            self.execute(api, password="invalid")


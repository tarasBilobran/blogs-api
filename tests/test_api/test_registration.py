from urllib.parse import urlencode
import httpx
import pytest

from service.models.users import Users


class TestRegistration:
    def execute(self, api: httpx.Client):
        response = api.post(
            "/api/v1/auth/registration",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(
                {
                    "email": "test@example.com",
                    "username": "test",
                    "password": "qwerty123",
                }
            ),
        )
        response.raise_for_status()
        return response

    def test_registration_saves_user_in_db(self, api, db_session):
        response = self.execute(api)
        assert response.status_code == 200, response.text

        user = db_session.query(Users).first()
        assert user.email == "test@example.com"
        assert user.username == "test"
        # Ensure password is not stored as plain text
        assert user.password_hash != "qwerty123"


    def test_user_already_exist(self, api):
        # First request must pass
        self.execute(api)

        # Second must fail with error
        with pytest.raises(httpx.HTTPStatusError, match="403 Forbidden"):
            self.execute(api)

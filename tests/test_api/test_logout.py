import uuid

from service.auth.hashing import hash_password
from service.models.session_tokens import SessionTokens
from service.models.users import Users
from service.tokens import generate_access_token


class TestLogout:
    def test_login_returns_jwt_pair(self, db_session, api, set_testing_settings):
        user = Users(id=uuid.uuid4(), username="test1", email="test@example.com", password_hash=hash_password("qwerty123"))
        token = generate_access_token(
            user.id,
            set_testing_settings.jwt
        )
        session_token = SessionTokens(
            token=token,
            user_id=user.id
        )
        db_session.add(user)
        db_session.commit()
        db_session.add(session_token)
        db_session.commit()

        response = api.post("/api/v1/auth/logout", headers={"authorization": f"Bearer {token}"})
        assert response.status_code == 200

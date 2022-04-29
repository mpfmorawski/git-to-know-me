from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi import HTTPException
from uuid import UUID
from .session_data import SessionData
from ..database.database import get_db
from ..database.database_operations import get_user


class Verifier(SessionVerifier[UUID, SessionData]):

    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception
        self._user_db = get_db()

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    @property
    def user_db(self):
        return self._user_db

    def verify_session(self, model: SessionData) -> bool:
        user = get_user(next(self.user_db), model.id)
        existing_ids = self.backend.data.values()
        if model in existing_ids and user:
            return True
        else:
            return False

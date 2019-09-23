from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.utils.functional import cached_property
from django.conf import settings
from redis import Redis


class SessionStore(SessionBase):

    @cached_property
    def __connection(self):
        return Redis(
            host=settings.SESSIONS_REDIS_HOST,
            port=settings.SESSIONS_REDIS_PORT,
            db=settings.SESSIONS_REDIS_DB,
            decode_responses=True
        )

    def load(self):
        try:
            data = self.__connection.get(self._get_or_create_session_key())
            return self.decode(session_data)
        except:
            self._session_key = None
            return {}

    def exists(self, session_key):
        return self.__connection.exists(session_key)

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            
            try:
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        if must_create and self.exists(self._get_or_create_session_key()):
            raise CreateError
        data = self.encode(self._get_session(no_load=must_create))
        self.__connection.setex(
            self._get_or_create_session_key(),
            self.get_expiry_age(),
            data
        )

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            self.__connection.delete(session_key)
        except:
            pass
        

    def clear_expired(self):
        pass

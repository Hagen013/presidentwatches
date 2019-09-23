from django.contrib.sessions.backends.base import SessionBase
from django.utils.functional import cached_property
from django.conf import settings
from redis import Redis


class SessionStore(SessionBase):

    @cached_property
    def _connection(self):
        return Redis(
            host=settings.SESSIONS_REDIS_HOST,
            port=settings.SESSIONS_REDIS_PORT,
            db=settings.SESSIONS_REDIS_DB,
            decode_responses=True
        )

    def load(self):
        # Получение данных сессии по ключу
        # Возвращает dict
        return self._connection.hgetall(self.session_key)

    def exists(self, session_key):
        # Проверка существования ключа сессии
        return self._connection.exists(session_key)

    def create(self):
        # Создание новой сессии
        self._session_key = self._get_new_session_key()
        self.save(must_create=True)
        self.modified = True

    def save(self, must_create=False):
        # Сохраняет данные сессии. Если аргумент `must_create`
        # Выставлен в True - создает новый объект, иначе только обновляет
        # существующий и не создает новый
        if self.session_key is None:
            return self.create()
        data = self._get_session(no_load=must_create)
        session_key = self._get_or_create_session_key()
        self._connection.hmset(session_key, data)
        self._connection.expire(session_key, self.get_expiry_age())

    def delete(self, session_key=None):
        # Удаляет данные сессии по указанному ключу
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        self._connection.delete(session_key)

    @classmethod
    def clear_expired(cls):
        # Не требуется удалять устаревшие ключи вручную,
        # поскольку этим занимается Redis

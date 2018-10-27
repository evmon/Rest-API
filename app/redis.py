from redis import StrictRedis
from django.conf import settings


class RedisClient:

    def __init__(self):
        self.connection = connection = StrictRedis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
        self._include_connection_methods(connection)

    def _include_connection_methods(self, connection):
        """Adds StrictRedis methods to the RedisClient as if we used StrictRedis as a base."""
        for attr in dir(connection):
            value = getattr(connection, attr)
            if attr.startswith('_') or not callable(value):
                continue
            self.__dict__[attr] = value


redis_client = RedisClient()

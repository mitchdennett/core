""" Session Redis Module """

import json

from masonite.contracts import SessionContract
from masonite.drivers.BaseSessionDriver import BaseSessionDriver
from masonite.request import Request
from masonite.app import App

from masonite.exceptions import DriverLibraryNotFound


class SessionRedisDriver(BaseSessionDriver, SessionContract):
    """Cookie Session Driver
    """

    def __init__(self, request: Request, app: App):
        """Redis Session Constructor

        Arguments:
            Environ {dict} -- The WSGI environment
            Request {masonite.request.Request} -- The Request class.
        """
        super().__init__(app)

        config = self.config.DRIVERS['redis']

        try:
            import redis
            self.redis = redis
        except ImportError:
            raise DriverLibraryNotFound(
                "Could not find the 'redis' library. Run pip install redis to fix this.")

        self.connection = redis.Redis(
            host=config['host'],
            port=config['port'],
            password=config['password'],
            decode_responses=True)

    def get(self, key):
        """Get a value from the session.

        Arguments:
            key {string} -- The key to get from the session.

        Returns:
            string|None - Returns None if a value does not exist.
        """

        ip = self._get_client_address()

        value = self.connection.hget('{0}_session'.format(ip), key)

        flash_value = self.connection.hget('{0}_flash'.format(ip), key)

        if flash_value:
            return self._get_serialization_value(flash_value)

        if value:
            return self._get_serialization_value(value)

        return None

    def set(self, key, value):
        """Set a vlue in the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """

        if isinstance(value, dict):
            value = json.dumps(value)

        ip = self._get_client_address()

        self.connection.hset('{0}_session'.format(ip), key, value)
        self.connection.expire('{0}_session'.format(ip), 1200)

    def has(self, key):
        """Check if a key exists in the session

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """

        if self.get(key):
            return True
        return False

    def delete(self, key):
        """Delete a value in the session by it's key.

        Arguments:
            key {string} -- The key to find in the session.

        Returns:
            bool -- If the key was deleted or not
        """
        ip = self._get_client_address()

        count = self.connection.hdel('{0}_session'.format(ip), key)
        if count > 0:
            return True

        return False

    def _collect_data(self):
        """Collect data from session and flash data

        Returns:
            dict
        """
        ip = self._get_client_address()
        session = self.connection.hgetall('{0}_session'.format(ip))
        flash = self.connection.hgetall('{0}_flash'.format(ip))

        session.update(flash)

        return session

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """

        if isinstance(value, dict):
            value = json.dumps(value)

        ip = self._get_client_address()

        self.connection.hset('{0}_flash'.format(ip), key, value)

    def reset(self, flash_only=False):
        """Deletes all session data

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """

        ip = self._get_client_address()

        if flash_only == False:
            self.connection.delete('{0}_session'.format(ip))

        self.connection.delete('{0}_flash'.format(ip))

    def helper(self):
        """Used to create builtin helper function
        """

        return self

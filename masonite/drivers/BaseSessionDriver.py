"""Base session driver module.
"""

import json

from masonite.drivers.BaseDriver import BaseDriver
from masonite.app import App


class BaseSessionDriver(BaseDriver):
    """Base session driver class. This class is inherited by all session drivers.
    """

    def __init__(self, app: App):
        """Base mail driver constructor.

        Arguments:
            SessionConfig {module} -- This is the config.session module.
            View {object} -- This is the masonite.view.View class.
        """

        self.config = app.make('SessionConfig')
        self.environ = app.make('Environ')

    def all(self):
        """Get all session data

        Returns:
            dict
        """

        return self._collect_data()

    def _get_serialization_value(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return value

    def _get_client_address(self):
        """
        Get ip from the client
        """

        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()

        return self.environ['REMOTE_ADDR']

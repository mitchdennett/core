""" Session Settings """

import os

"""
|--------------------------------------------------------------------------
| Session Driver
|--------------------------------------------------------------------------
|
| Sessions are able to be linked to an individual user and carry data from
| request to request. The memory driver will store all the session data
| inside memory which will delete when the server stops running.
|
| Supported: 'memory', 'cookie', 'redis'
|
"""

DRIVER = os.getenv('SESSION_DRIVER', 'memory')


DRIVERS = {
    'redis': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': os.getenv('REDIS_PORT', '6379'),
        'password': os.getenv('REDIS_PASSWORD', '')
    }
}

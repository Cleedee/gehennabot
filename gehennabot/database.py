import os
from dotenv import dotenv_values

from masoniteorm.connections.ConnectionResolver import ConnectionResolver

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
ambiente = dotenv_values(env_path)

DATABASES = {
    'default': 'sqlite',
    'sqlite': {
        'driver': 'sqlite',
        'database': ambiente['DATABASE_URL'],
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)

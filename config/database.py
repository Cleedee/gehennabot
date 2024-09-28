from dotenv import dotenv_values

from masoniteorm.connections.ConnectionResolver import ConnectionResolver

ambiente = dotenv_values('.env')

DATABASES = {
    'default': 'sqlite',
    'sqlite': {
        'driver': 'sqlite',
        'database': ambiente['DATABASE_URL'],
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)

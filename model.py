from orator import DatabaseManager, Model

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': '/home/claudio/Projetos/Python/web2py_37/web2py/applications/Gehenna/databases/storage.sqlite',
    }
}

db = DatabaseManager(config)

Model.set_connection_resolver(db)

class Carta(Model):
    __table__ = 'cartas'

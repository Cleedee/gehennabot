from orator import DatabaseManager, Model
from orator.orm import has_one

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': '/home/claudio/Projetos/Python/web2py_37/web2py/applications/Gehenna/databases/storage.sqlite',
    }
}

db = DatabaseManager(config)

Model.set_connection_resolver(db)

class Usuario(Model):
    __table__ = 'auth_user'

class Carta(Model):
    __table__ = 'cartas'

class Estoque(Model):
    __table__ = 'estoques'

    @has_one
    def dono(self):
        return Usuario

    @has_one
    def carta(self):
        return Carta

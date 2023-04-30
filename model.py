from orator import DatabaseManager, Model
from orator.orm import has_one, belongs_to, belongs_to_many
from dotenv import dotenv_values

ambiente = dotenv_values(".env")

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': ambiente['DATABASE_URL'],
    }
}

db = DatabaseManager(config)

Model.set_connection_resolver(db)

class Estoque(Model):
    __table__ = 'estoques'

class Usuario(Model):
    __table__ = 'auth_user'

class Carta(Model):
    __table__ = 'cartas'
    __timestamps__ = False

    @belongs_to_many('estoques','carta','dono')
    def donos(self):
        return Usuario

class Deck(Model):
    ...

class Composicao(Model):
    __table__ = 'composicao'

class Entrada(Model):
    __table__ = 'entradas'

class ItemEntrada(Model):
    __table__ = 'detalhes'

class Saida(Model):
    __table__ = 'saidas'

class ItemSaida(Model):
    __table__ = 'itens_saida'

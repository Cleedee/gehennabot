from dotenv import dotenv_values
from orator import DatabaseManager, Model
from orator.orm import belongs_to_many, has_many, has_one

GRUPOS = ['1', '2', '3', '4', '5', '6', '7', 'ANY']

ambiente = dotenv_values('.env')

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

    @belongs_to_many('estoques', 'carta', 'dono')
    def donos(self):
        return Usuario


class Deck(Model):
    __timestamps__ = False

    @has_many('deck')
    def composicao(self):
        return Composicao


class Composicao(Model):
    __table__ = 'composicao'
    __timestamps__ = False


class Entrada(Model):
    __table__ = 'entradas'


class ItemEntrada(Model):
    __table__ = 'detalhes'


class Saida(Model):
    __table__ = 'saidas'


class ItemSaida(Model):
    __table__ = 'itens_saida'

    @has_one('carta')
    def carta(self):
        return Carta

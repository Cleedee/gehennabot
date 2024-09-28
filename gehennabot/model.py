from dotenv import dotenv_values
from masoniteorm.models import Model
from masoniteorm.connections import ConnectionResolver
from masoniteorm.relationships import belongs_to_many, has_many

ambiente = dotenv_values('.env')

DATABASES = {
    'default': 'sqlite',
    'sqlite': {
        'driver': 'sqlite',
        'database': ambiente['DATABASE_URL'],
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
GRUPOS = ['1', '2', '3', '4', '5', '6', '7', 'ANY']

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
    __timestamps__ = False


class ItemEntrada(Model):
    __table__ = 'detalhes'
    __timestamps__ = False


class Saida(Model):
    __table__ = 'saidas'


class ItemSaida(Model):
    __table__ = 'itens_saida'

#    @has_one('carta')
#    def carta(self):
#        return Carta

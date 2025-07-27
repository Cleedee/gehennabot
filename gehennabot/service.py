from typing import Any, List, Tuple, Union, Dict
from datetime import date

from masoniteorm.query import QueryBuilder

from gehennabot import api, util
from gehennabot.model import Carta, Deck, ItemEntrada, Usuario
from gehennabot.schemas import Item
from gehennabot.sources import select_search_strategy

def procurar_usuario(username):
    return api.procurar_usuario(username)

def procurar_usuarios():
    return api.procurar_usuarios()

def procurar_usuario_por_id(id):
    return api.procurar_usuario_por_id(id)

def estoque_da_carta(usuario, carta):
    return api.estoque_da_carta(usuario['username'], carta['id'])

def total_estoque(username):
    return api.total_estoque(username)

def entradas_por_usuario(username):
    return api.entradas_por_usuario(username)

def itens_por_movimentacao(movimentacao_id):
    return api.itens_por_movimentacao(movimentacao_id)

def movimentacao_por_id(movimentacao_id):
    return api.movimentacao_por_id(movimentacao_id)

def saidas_por_usuario(username):
    return api.saidas_por_usuario(username)

def procurar_donos_da_carta(card_id):
    return api.procurar_donos(card_id)

def procurar_carta(id: int):
    return api.procurar_carta_por_id(id)

def procurar_carta_por_nome(nome: str) -> dict:
    carta = api.procurar_carta_por_nome(nome)
    return carta

def procurar_cartas_por_nome(nome: str) -> list[dict]:
    return api.procurar_cartas_por_nome(nome)

def procurar_cartas_por_ids(ids: list[int]):
    return api.procurar_cartas_por_ids(ids)

def todas_as_cartas() -> list[dict]:
    return api.procurar_cartas_todas()

def decks_por_usuario(username: str) -> list[dict]:
    decks = api.procurar_decks_por_usuario(username)
    return decks

def deck_por_id(deck_id):
    return api.procurar_deck_por_id(deck_id)

def deck_por_code(code):
    return api.procurar_deck_por_code(code)

def decks_preconstruidos():
    return api.procurar_decks_preconstruidos()

def decks_por_nome(usuario, nome):
    return api.procurar_decks_por_nome(usuario, nome)

def cadastrar_deck(deck: Dict, slots: List[Dict]) -> Dict:
    deck = api.cadastrar_deck(deck)
    for slot in slots:
        slot['deck_id'] = deck['id']
        api.cadastrar_slot(slot)
    return deck

def atualizar_deck(deck: Dict):
    api.atualizar_deck(deck)

def apagar_deck(deck_id):
    api.apagar_deck(deck_id)

def extrair_deck_da_internet(url, usuario) -> Tuple[Dict, List]:
    slots = select_search_strategy(url)
    if not slots:
        return ({}, [])
    print(slots)
    deck = {
        'name': 'Novo Deck',
        'description': url,
        'tipo': 'other',
        'owner_id': usuario['id'],
        'code': 0
    }
    nao_encontradas = 'Não encontradas pelo bot RutorsHandBot:\n'
    itens = []
    for key in slots.keys():
        carta = api.procurar_carta_por_codevdb(key)
        if carta:
            item = {
                'quantity': int(slots[key]),
                'card_id': carta['id'],
                'code': 0
            }
            itens.append(item)
        else:
            nao_encontradas += f"\n{slots[key]} x {key}"
            deck['description'] = nao_encontradas
    #slots_deck = slots_por_deck(deck['id'])
    #nome = util.sugestao_nome_deck(slots_deck)
    #deck['name'] = nome
    #api.atualizar_deck(deck)
    return deck, itens


def slots_por_deck(deck_id):
    return api.procurar_slots_por_deck(deck_id)

def adicionar_deck_como_entrada(deck_id: int, usuario: Dict):
    deck = deck_por_id(deck_id)
    slots = slots_por_deck(deck_id)
    movimento: Dict = {
        'name': deck['name'],
        'tipo': 'E',
        'owner_id': usuario['id'],
        'date_move': date.today().isoformat(),
        'price': '0.0',
        'code': 0
    }
    movimento_cadastrado = api.cadastrar_movimento(movimento)
    if not movimento_cadastrado:
        return {}
    # cadastrar itens de um movimento de entrada 
    for slot in slots:
        item = Item(
            slot['card_id'],
            movimento_cadastrado['id'],
            slot['quantity'],
            0
        )
        api.cadastrar_item(item)
    # card_id: int
    # moviment_id: int
    # quantity: int
    # code: int
    return movimento_cadastrado

def legado_procurar_carta(id: int) -> Carta:
    return Carta.find(id)

def legado_todas_as_cartas() -> List[Carta]:
    return Carta.all()

def legado_estoques_por_carta(codigo) -> List[str]:
    carta = Carta.find(codigo)
    codigo_usuarios = [dono.username for dono in carta.donos]
    return codigo_usuarios

def legado_decks_por_usuario(username) -> List[Deck]:
    usuario = Usuario.where('username', username).first()
    if usuario:
        decks = Deck.where('dono', usuario.id).get()
        return decks
    return []

def legado_deck_por_id(id) -> Union[Deck, None]:
    return Deck.find(id)

def legado_decks_por_nome(username: str, nome_deck: str) -> List[Deck]:
    decks = legado_decks_por_usuario(username)
    return [
        deck for deck in decks if nome_deck in deck.nome
    ]

def legado_composicao_deck(deck_id):
    builder = QueryBuilder().table('composicao')
    composicao = (
        builder.join('cartas', 'composicao.carta', '=', 'cartas.id')
        .select(
            'composicao.quantidade as quantidade',
            'cartas.nome as nome',
            'cartas.grupo as grupo',
            'cartas.id as carta',
            'cartas.tipo as tipo',
            'cartas.clan as clan',
            'composicao.deck as deck',
            'composicao.id as id'
        )
        .where('composicao.deck', deck_id)
        .get().all()
    )
    return composicao

def legado_itens_entrada_por_entrada_id(id: int) -> List[ItemEntrada]:
    return ItemEntrada.where('entrada', id).get()

def total_decks(username: str) -> int:
    usuario = Usuario.where('username', username).first()
    if usuario:
        return Deck.where('dono', usuario.id).count()
    return 0

def cartas_que_faltam_para_o_deck():
    return

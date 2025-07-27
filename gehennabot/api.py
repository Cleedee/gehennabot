from typing import Dict
import requests

from gehennabot.schemas import Item

URL = 'http://localhost:8002'

def movimentacoes_por_usuario(username: str):
    r = requests.get(f'{URL}/stocks/moviments/{username}')
    return r.json()['moviments']

def cadastrar_movimento(movimento: Dict) -> dict:
    r = requests.post(f'{URL}/stocks/moviments', json=movimento)
    if r.status_code == 201:
        return r.json()
    return {}

def cadastrar_item(item: Item) -> Dict:
    r = requests.post(f'{URL}/stocks/items', json=item._asdict())
    if r.status_code == 201:
        return r.json()
    return {}

def carta_por_codigo(codigo: str) -> dict:
    r = requests.get(f'{URL}/cards/?code={codigo}')
    return r.json()['cards'][0] if r.json()['cards'] else {}

def procurar_carta_por_id(id: int) -> dict:
    r = requests.get(f'{URL}/cards/{id}')
    if r.status_code == 404:
        return {}
    return r.json()

def procurar_carta_por_nome(nome: str) -> dict:
    r = requests.get(f'{URL}/cards/{nome}/name')
    if r.status_code == 404:
        return {}
    return r.json()

def procurar_cartas_por_nome(nome: str, pagina: int = 0, por_pagina = 100):
    r = requests.get(f'{URL}/cards/?name={nome}&skip={pagina}&limit={por_pagina}')
    return r.json()['cards']

def procurar_carta_por_codevdb(codevdb: int, pagina: int = 0, por_pagina = 100) -> Dict:
    r = requests.get(f'{URL}/cards/?codevdb={codevdb}')
    cartas = r.json()['cards']
    carta = cartas[0] if len(cartas) > 0 else {}
    return carta

def procurar_cartas_todas(pagina: int = 0, por_pagina: int = 100):
    r = requests.get(f'{URL}/cards/?skip={pagina}&limit={por_pagina}')
    return r.json()['cards']

def procurar_cartas_por_ids(ids : list[int]):
    query = '?ids='
    for i in ids:
        query += (str(i) + ',')
    r = requests.get(f'{URL}/cards/{query}')
    return r.json()['cards']

def procurar_usuario(username: str):
    r =requests.get(f'{URL}/users/{username}/by_name')
    return r.json()

def procurar_usuario_por_id(id: str):
    r = requests.get(f'{URL}/users/{id}')
    return r.json()

def procurar_usuarios():
    r = requests.get(f'{URL}/users')
    return r.json()['users']

def estoque_da_carta(username, card_id):
    r = requests.get(f'{URL}/stocks/cards/{card_id}/{username}')
    return r.json()['quantity']

def total_estoque(username: str):
    r = requests.get(f'{URL}/stocks/{username}/total')
    return r.json()['quantity']

def entradas_por_usuario(username):
    r = requests.get(f'{URL}/stocks/moviments/{username}?tipo=E')
    return r.json()['moviments']

def movimentacao_por_id(movimentacao_id):
    r = requests.get(f'{URL}/stocks/moviment/{movimentacao_id}')
    return r.json()

def itens_por_movimentacao(movimentacao_id):
    r = requests.get(f'{URL}/stocks/items/{movimentacao_id}')
    return r.json()['items']

def saidas_por_usuario(username):
    r = requests.get(f'{URL}/stocks/moviments/{username}?tipo=S')
    return r.json()['moviments']

def cadastrar_deck(deck: Dict) -> Dict:
    r = requests.post(f'{URL}/decks', json=deck)
    return r.json()

def atualizar_deck(deck: Dict) -> Dict:
    r = requests.put(f'{URL}/decks/{deck["id"]}', json=deck)
    if r.status_code == 404:
        return {}
    return r.json()

def apagar_deck(id: str):
    r = requests.delete(f'{URL}/decks/{id}')
    if r.status_code == 404:
        return {}
    return r.json()

def cadastrar_slot(slot: Dict) -> Dict:
    r = requests.post(f'{URL}/slots', json=slot)
    return r.json()

def procurar_decks_por_usuario(username:str):
    total = total_decks(username)
    r = requests.get(f'{URL}/decks?username={username}&limit={total}')
    return r.json()['decks']

def procurar_decks_por_nome(username: str, nome_deck: str):
    r = requests.get(f'{URL}/decks?username={username}&name={nome_deck}')
    return r.json()['decks']

def procurar_deck_por_id(id: str):
    r = requests.get(f'{URL}/decks/{id}')
    return r.json()

def procurar_deck_por_code(code: str):
    r = requests.get(f'{URL}/decks?code={code}')
    decks = r.json()['decks']
    if len(decks) > 0:
        return decks[0]
    return {}

def procurar_decks_preconstruidos():
    r = requests.get(f'{URL}/decks?preconstructed=True')
    return r.json()['decks']

def total_decks(username: str) -> int:
    r = requests.get(f'{URL}/decks/{username}/total')
    return int(r.json()['quantity'])

def procurar_slots_por_deck(deck_id: str):
    r = requests.get(f'{URL}/slots/{deck_id}/deck')
    return r.json()['slots']

def procurar_donos(card_id: str):
    r = requests.get(f'{URL}/stocks/owners/{card_id}')
    return r.json()['users']

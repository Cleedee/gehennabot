import requests

URL = 'http://localhost:8002'

def movimentacoes_por_usuario(username: str):
    r = requests.get(f'{URL}/stocks/moviments/{username}')
    return r.json()['moviments']

def carta_por_codigo(codigo: str) -> list[dict]:
    r = requests.get(f'{URL}/cards/?code={codigo}')
    return r.json()['cards'] or []

def procurar_carta_por_id(id: int) -> dict:
    r = requests.get(f'{URL}/cards/{id}')
    return r.json()

def procurar_carta_por_nome(nome: str) -> dict:
    r = requests.get(f'{URL}/cards/{nome}/name')
    return r.json()

def procurar_cartas_por_nome(nome: str, pagina: int = 0, por_pagina = 100):
    r = requests.get(f'{URL}/cards/?name={nome}&skip={pagina}&limit={por_pagina}')
    return r.json()['cards']

def procurar_cartas_todas(pagina: int = 0, por_pagina: int = 100):
    r = requests.get(f'{URL}/cards/?skip={pagina}&limit={por_pagina}')
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
    r = requests.get(f'{URL}/cards/{card_id}/{username}')
    return r.json()

def procurar_decks_por_usuario(username:str):
    r = requests.get(f'{URL}/decks/{username}')
    return r.json()['decks']

def procurar_deck_por_id(id: str):
    r = requests.get(f'{URL}/decks/{id}')
    return r.json()

def procurar_slots_por_deck(deck_id: str):
    r = requests.get(f'{URL}/slots/{deck_id}/deck')
    return r.json()['slots']

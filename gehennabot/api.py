import requests

URL = 'http://localhost:8002'

def movimentacoes_por_usuario(username: str):
    r = requests.get(f'{URL}/stocks/moviments/{username}')
    return r.json()['moviments']

def carta_por_codigo(codigo: str):
    r = requests.get(f'{URL}/card_by_code/{codigo}')
    return r.json()

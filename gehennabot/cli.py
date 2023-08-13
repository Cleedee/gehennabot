import typer
import requests

from gehennabot import service 
from gehennabot.model import Carta

app = typer.Typer()

@app.command()
def gehenna_api_create_card():
    lista: list[Carta] = service.todas_as_cartas()
    for carta in lista:
        print(carta.nome)
        json_carta = {
            'code': carta.id,
            'name': carta.nome,
            'tipo': carta.tipo,
            'disciplines': carta.disciplinas,
            'capacity': carta.capacidade,
            'clan': carta.clan,
            'attributes': '' if carta.atributos is None else carta.atributos,
            'group': '' if carta.grupo is None else str(carta.grupo),
            'sect': '' if carta.seita is None else carta.seita,
            'cost': '' if carta.custo is None else carta.custo,
            'text': '' if carta.descricao is None else carta.descricao,
            'title': '' if carta.titulo is None else carta.titulo,
        }
        print(json_carta)
        r = requests.post(
            'http://localhost:8002/cards',
            json=json_carta
        )
        print(f"Status code: {r.status_code}, Response: {r.json()}")

@app.command()
def todas_cartas():
    lista: list[Carta] = service.todas_as_cartas()
    print("[")
    for carta in lista:
        print("{")
        print('"code": "{}",'.format(carta.id))
        print('"name": "{}",'.format(carta.nome))
        print('"tipo": "{}",'.format(carta.tipo))
        print('"disciplines": "{}",'.format(carta.disciplinas))
        print('"capacity": "{}",'.format(carta.capacidade))
        print('"clan": "{}",'.format(carta.clan))
        print('"attributes": "{}",'.format("" if carta.atributos is None else carta.atributos))
        print('"group": "{}",'.format("" if carta.grupo is None else carta.grupo))
        print('"sect": "{}",'.format("" if carta.seita is None else carta.seita))
        print('"cost": "{}",'.format(carta.custo))
        print('"text": "{}",'.format(carta.descricao))
        print('"title": "{}"'.format("" if carta.titulo is None else carta.titulo))
        print("},")
    print("]")

@app.command()
def preconstruidos():
    lista = service.decks_preconstruidos()
    for deck in lista:
        print(deck.id, deck.nome)

@app.command()
def usuarios():
    lista = service.procurar_usuarios()
    for usuario in lista:
        print(usuario.username)

@app.command()
def adicionar_precon(deck_id: int, dono: str):
    entrada = service.adicionar_deck_como_entrada(deck_id, dono)
    if entrada:
        print('Nova entrada incluída.')
    else:
        print('Deck preconstruído não pôde ser adicionado.')

@app.command()
def procura_carta(nome: str):
    lista = service.procurar_cartas_por_nome(nome)
    for carta in lista:
        print(carta.id, carta.nome)

@app.command()
def decks(nome: str, username='torcato'):
    lista = service.decks_por_nome(username, nome)
    for deck in lista:
        print(deck.id, deck.nome)

@app.command()
def adicionar(deck_id: int, carta_id: int, quantidade: int):
    service.adicionar_cartas_ao_deck(deck_id, carta_id, quantidade)
    print('Cartas adicionadas.')

@app.command()
def falta(deck_id: int):
    deck = service.deck_por_id(deck_id)
    faltantes = service.cartas_que_faltam_para_o_deck(deck)
    for id, nome, quantidade in faltantes:
        print(quantidade, f"({id}) {nome}")

@app.command()
def falta_e_procura(deck_id: int):
    deck = service.deck_por_id(deck_id)
    faltantes = service.cartas_que_faltam_para_o_deck(deck)
    decks = service.procurar_cartas_em_preconstruidos([id for (id, _, _) in faltantes])
    for deck in decks:
        print(deck[0])
        for carta in deck[1]:
            print('    ',carta)

@app.command()
def copiar_deck(deck_id: int):
    id = service.criar_copia_deck(deck_id)
    print('Deck copiado com id', id)

@app.command()
def baixar_internet(url, username):
    usuario = service.procurar_usuario(username)
    deck = service.extrair_deck_da_internet(url, usuario)
    print(deck.nome, 'importado com id', deck.id)

def preconstruido_como_saida(deck_id, dono_id):
    ...

if __name__ == "__main__":
    app()

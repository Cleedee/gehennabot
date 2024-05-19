from datetime import datetime 

import requests
import typer
from rich.console import Console
from rich.table import Table

from gehennabot import service, sources
from gehennabot.model import Carta
from gehennabot  import api

app = typer.Typer()

@app.command()
def gehenna_api_create_item(username: str):
    movimentacoes = api.movimentacoes_por_usuario(username)
    for movimentacao in movimentacoes:
        if movimentacao['tipo'] == 'E':
            itens = service.legado_itens_entrada_por_entrada_id(movimentacao['code'])
            for item in itens:
                print(f'Carta: {item.carta}')
                carta = api.carta_por_codigo(item.carta)
                json_item = {
                    'moviment_id': movimentacao['id'],
                    'card_id': carta['id'],
                    'quantity': item.quantidade,
                    'code': item.id
                }
                r = requests.post('http://localhost:8002/stocks/items', json=json_item)
        else:
            codigo_subtraido = movimentacao['code'] - 1000
            itens = service.legado_itens_saida_por_saida_id(codigo_subtraido)
            for item in itens:
                carta = api.carta_por_codigo(item.carta)
                json_item = {
                    'moviment_id': movimentacao['id'],
                    'card_id': carta['id'],
                    'quantity': item.quantidade,
                    'code': item.id
                }
                r = requests.post('http://localhost:8002/stocks/items', json=json_item)

@app.command()
def gehenna_api_create_moviment(username: str):
    usuario = service.legado_procurar_usuario(username)
    entradas = service.legado_entradas_por_usuario(usuario)
    saidas = service.legado_saidas_por_usuario(usuario)
    for entrada in entradas:
        json_move = {
            'name': entrada.origem,
            'tipo': 'E',
            'date_move': entrada.data,
            'owner_id': entrada.dono,
            'price': entrada.preco if entrada.preco else 0.0,
            'code': entrada.id 
        }
        r = requests.post('http://localhost:8002/stocks/moviments', json=json_move)
        print(f'Status code: {r.status_code}, Response: {r.json()}')
    for saida in saidas:
        date_object = datetime.strptime(
            saida.data_cadastro,
            '%Y-%m-%d %H:%M:%S'
        ).date().strftime('%Y-%m-%d')
        json_move = {
            'name': saida.descricao + '[' + saida.tipo if saida.tipo else '' + ']',
            'tipo': 'S',
            'date_move': date_object,
            'owner_id': saida.dono,
            'price': 0.0,
            'code': saida.id + 1000
        }
        r = requests.post('http://localhost:8002/stocks/moviments', json=json_move)
        print(f'Status code: {r.status_code}, Response: {r.json()}')

@app.command()
def gehenna_api_create_card():
    lista: list[Carta] = service.legado_todas_as_cartas()
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
        r = requests.post('http://localhost:8002/cards', json=json_carta)
        print(f'Status code: {r.status_code}, Response: {r.json()}')

@app.command()
def gehenna_api_create_deck(username: str):
    decks = service.legado_decks_por_usuario(username)
    for deck in decks:
        json_deck =  {
            'name': deck.nome,
            'description': deck.descricao,
            'creator': deck.criador,
            'player': deck.jogador,
            'tipo': deck.tipo,
            'created': deck.data_cadastro,
            'updated': deck.ultima_atualizacao,
            'preconstructed': deck.preconstruido or False,
            'owner_id': deck.dono,
            'code': deck.id
        }
        print(json_deck)
        r = requests.post('http://localhost:8002/decks', json=json_deck)
        print(f'Status code: {r.status_code}, Response: {r.json()}')

@app.command()
def gehenna_api_create_slot(username: str):
    decks = service.decks_por_usuario(username)
    for deck in decks:
        slot = service.legado_composicao_deck(deck['code'])
        json_slot = {
            'deck_id': slot.deck,
            'card_id': slot.carta,
            'quantity': slot.quantidade
        }
        print(json_slot)
        r = requests.post("http://localhost:8002/slots/{deck['id']}", json=json_slot)
        print(f'Status code: {r.status_code}, Response: {r.json()}')

@app.command()
def todas_cartas():
    lista: list[Carta] = service.legado_todas_as_cartas()
    print('[')
    for carta in lista:
        print('{')
        print('"code": "{}",'.format(carta.id))
        print('"name": "{}",'.format(carta.nome))
        print('"tipo": "{}",'.format(carta.tipo))
        print('"disciplines": "{}",'.format(carta.disciplinas))
        print('"capacity": "{}",'.format(carta.capacidade))
        print('"clan": "{}",'.format(carta.clan))
        print(
            '"attributes": "{}",'.format(
                '' if carta.atributos is None else carta.atributos
            )
        )
        print(
            '"group": "{}",'.format('' if carta.grupo is None else carta.grupo)
        )
        print(
            '"sect": "{}",'.format('' if carta.seita is None else carta.seita)
        )
        print('"cost": "{}",'.format(carta.custo))
        print('"text": "{}",'.format(carta.descricao))
        print(
            '"title": "{}"'.format(
                '' if carta.titulo is None else carta.titulo
            )
        )
        print('},')
    print(']')


@app.command()
def preconstruidos():
    lista = service.legado_decks_preconstruidos()
    for deck in lista:
        print(deck.id, deck.nome)


@app.command()
def usuarios():
    lista = service.procurar_usuarios()
    for usuario in lista:
        print(usuario.username)


@app.command()
def adicionar_precon(deck_id: int, dono: str):
    entrada = service.legado_adicionar_deck_como_entrada(deck_id, dono)
    if entrada:
        print('Nova entrada incluída.')
    else:
        print('Deck preconstruído não pôde ser adicionado.')


@app.command()
def procura_carta(nome: str):
    lista = service.legado_procurar_cartas_por_nome(nome)
    for carta in lista:
        print(carta.id, carta.nome)

@app.command()
def procura_carta_id(id: int):
    carta = service.legado_procurar_carta(id)
    print(carta.id, carta.nome)

@app.command()
def decks(nome: str, username='torcato'):
    table = Table(title=f'Decks de {username}')
    lista = service.legado_decks_por_nome(username, nome)
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="cyan")
    for deck in lista:
        table.add_row(str(deck.id), deck.nome)
    console = Console()
    console.print(table)

@app.command()
def adicionar(deck_id: int, carta_id: int, quantidade: int):
    service.legado_adicionar_cartas_ao_deck(deck_id, carta_id, quantidade)
    print('Cartas adicionadas.')


@app.command()
def falta(deck_id: int):
    deck = service.legado_deck_por_id(deck_id)
    faltantes = service.legado_cartas_que_faltam_para_o_deck(deck)
    for id, nome, quantidade in faltantes:
        print(quantidade, f'({id}) {nome}')


@app.command()
def falta_e_procura(deck_id: int):
    deck = service.legado_deck_por_id(deck_id)
    faltantes = service.legado_cartas_que_faltam_para_o_deck(deck)
    decks = service.legado_procurar_cartas_em_preconstruidos(
        [id for (id, _, _) in faltantes]
    )
    for deck in decks:
        print(deck[0])
        for carta in deck[1]:
            print('    ', carta)


@app.command()
def copiar_deck(deck_id: int):
    id = service.legado_criar_copia_deck(deck_id)
    print('Deck copiado com id', id)


@app.command()
def baixar_internet(url, username):
    usuario = service.legado_procurar_usuario(username)
    deck = service.legado_extrair_deck_da_internet(url, usuario)
    print(deck.nome, 'importado com id', deck.id)


@app.command()
def deck_vdb(url):
    resposta = sources.slots_from_vdb(url)
    print(resposta)

def preconstruido_como_saida(deck_id, dono_id):
    ...


if __name__ == '__main__':
    app()

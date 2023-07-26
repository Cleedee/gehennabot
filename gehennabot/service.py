from collections import namedtuple
from datetime import date

import requests

import util
from model import (Carta, Composicao, Deck, Entrada, Estoque, ItemEntrada,
                   ItemSaida, Saida, Usuario, db)


def procurar_usuario(username):
    return Usuario.where('username', '=', username).first()

def procurar_usuario_por_id(id):
    return Usuario.find(id)

def procurar_usuarios():
    return Usuario.get()

def estoque_da_carta(usuario, carta):
    soma_entradas = (
        db.table('detalhes')
        .join('entradas', 'entradas.id', '=', 'detalhes.entrada')
        .where('detalhes.carta', '=', carta.id)
        .where('entradas.dono', '=', usuario.id)
        .sum('detalhes.quantidade')
    )
    soma_saidas = (
        db.table('itens_saida')
        .join('saidas', 'saidas.id', '=', 'itens_saida.saida')
        .where('itens_saida.carta', '=', carta.id)
        .where('saidas.dono', '=', usuario.id)
        .sum('itens_saida.quantidade')
    )
    soma_entradas = soma_entradas if soma_entradas else 0
    soma_saidas = soma_saidas if soma_saidas else 0
    total = soma_entradas - soma_saidas
    return total


def total_estoque(username) -> int:
    usuario = procurar_usuario(username)
    total = 0
    total = (
        db.table('estoques').where('dono', '=', usuario.id).sum('quantidade')
    )
    return total


def procurar_carta(codigo) -> Carta:
    return Carta.find(codigo)


def procurar_carta_serializada(nome: str) -> dict:
    carta = Carta.where('nome', '=', nome).first()
    return carta.serialize() if carta else {}


def procurar_carta_por_nome(nome: str) -> Carta:
    return Carta.where('nome', '=', nome).first()

def procurar_cartas_por_nome(nome: str) -> list[Carta]:
    return Carta.where('nome','like',f'%{nome}%').get()

def estoques_por_carta(codigo) -> list[str]:
    carta = Carta.find(codigo)
    codigo_usuarios = [dono.username for dono in carta.donos]
    return codigo_usuarios


def decks_por_usuario(username):
    usuario = Usuario.where('username', '=', username).first()
    if usuario:
        decks = Deck.where('dono', '=', usuario.id).get()
        return decks
    return []


def deck_por_id(id) -> Deck | None:
    return Deck.find(id)

def decks_por_nome(username: str, nome_deck: str) -> list[Deck]:
    decks = decks_por_usuario(username)
    return [deck for deck in decks if nome_deck in deck.nome]

def decks_preconstruidos():
    return Deck.where('preconstruido', '=', 'T').get()

def adicionar_cartas_ao_deck(deck_id: int, carta_id: int, quantidade: int):
    c = Composicao()
    c.quantidade = quantidade
    c.deck = deck_id
    c.carta = carta_id
    c.save()
    
def composicao_deck(id: int) -> list[Composicao]:
    composicao = (
        db.table('composicao')
        .join('cartas', 'composicao.carta', '=', 'cartas.id')
        .select(
            'composicao.quantidade',
            'cartas.nome',
            'cartas.grupo',
            'cartas.id',
            'cartas.tipo',
            'cartas.clan',
        )
        .where('composicao.deck', '=', id)
        .get()
    )
    return composicao


def composicoes_deck_por_id(id: int) -> list[Composicao]:
    return Composicao.where('deck', '=', id).get()


def extrair_deck_da_internet(url, usuario) -> Deck | None:
    r = requests.get(url)
    if r.status_code != 200:
        return None
    texto = r.text
    linhas = [linha for linha in texto.split('\n') if '\t' in linha]
    Slot = namedtuple('Slot', 'quantidade nome')
    slots = [Slot(*linha.split('\t')) for linha in linhas]
    novo_deck = Deck()
    novo_deck.nome = 'Novo deck'
    novo_deck.descricao = url
    novo_deck.tipo = 'other'
    novo_deck.dono = usuario.id
    novo_deck.save()
    nao_encontradas = 'Não encontradas pelo bot RutorsHandBot:\n'
    for slot in slots:
        carta = procurar_carta_por_nome(slot.nome)
        if carta:
            c = Composicao()
            print(novo_deck.id)
            c.deck = novo_deck.id
            c.quantidade = int(slot.quantidade)
            c.carta = carta.id
            c.save()
        else:
            nao_encontradas += f'\n{slot.quantidade} x {slot.nome}'
            novo_deck.descricao = nao_encontradas
    composicao = composicao_deck(novo_deck.id)
    nome = util.sugestao_nome_deck(composicao)
    novo_deck.nome = nome
    novo_deck.save()
    return novo_deck


def entradas_por_usuario(usuario):
    return Entrada.where('dono', '=', usuario.id).get()


def saidas_por_usuario(usuario):
    return Saida.where('dono', '=', usuario.id).get()


def entrada_por_id(id: int) -> Entrada:
    return Entrada.find(id)


def saida_por_id(id: int) -> Saida:
    return Saida.find(id)


def detalhe_entrada(entrada_id) -> str:
    entrada = entrada_por_id(entrada_id)
    texto = '\n'.join(
        [
            '**Entrada ID:** {id}',
            '**Origem:** {origem}',
            '**Data:** {data}',
            '**Preço:** {preco}',
        ]
    )
    texto = texto.format(
        id=entrada.id,
        origem=entrada.origem,
        data=entrada.data,
        preco=entrada.preco,
    )
    itens_entrada = (
        db.table('detalhes')
        .join('cartas', 'detalhes.carta', '=', 'cartas.id')
        .select('detalhes.quantidade', 'detalhes.preco', 'cartas.nome')
        .where('detalhes.entrada', '=', entrada_id)
        .order_by('cartas.tipo')
        .get()
    )
    texto_cartas = '\n'.join(
        [f'{item.quantidade} x {item.nome}' for item in itens_entrada]
    )
    return texto + '\n\n' + texto_cartas


def detalhe_saida(saida_id) -> str:
    saida = saida_por_id(saida_id)
    texto = '\n'.join(
        [
            '**Saida ID:** {id}',
            '**Descrição:** {descricao}',
            '**Data:** {data}',
            '**Tipo:** {tipo}',
        ]
    )
    texto = texto.format(
        id=saida.id,
        descricao=saida.descricao,
        data=saida.data_cadastro,
        tipo=saida.tipo,
    )
    itens_saida = (
        db.table('itens_saida')
        .join('cartas', 'itens_saida.carta', '=', 'cartas.id')
        .select('itens_saida.quantidade', 'itens_saida.preco', 'cartas.nome')
        .where('itens_saida.saida', '=', saida_id)
        .order_by('cartas.tipo')
        .get()
    )
    texto_cartas = '\n'.join(
        [f'{item.quantidade} x {item.nome}' for item in itens_saida]
    )
    return texto + '\n\n' + texto_cartas

def adicionar_deck_como_entrada(deck_id: int, username: str):
    with db.transaction():
        deck = deck_por_id(deck_id)
        composicao = composicao_deck(deck.id)
        usuario = procurar_usuario(username)
        entrada = Entrada()
        entrada.data = date.today()
        entrada.origem = deck.nome
        entrada.preco = 0
        entrada.dono = usuario.id
        entrada.save()
        for slot in composicao:
            item = ItemEntrada()
            item.entrada = entrada.id
            item.quantidade = slot.quantidade
            item.carta = slot.id
            item.preco = 0
            item.save()
    return entrada

def cartas_que_faltam_para_o_deck(deck: Deck):
    faltantes = []
    usuario = procurar_usuario_por_id(deck.dono)
    # trazer a composição do deck
    composicoes = composicoes_deck_por_id(deck.id)
    # comparar cada slot com o estoque
    for composicao in composicoes:
        carta = procurar_carta(composicao.carta)
        estoque = estoque_da_carta(usuario, carta)
        diferenca = estoque - composicao.quantidade
        if diferenca < 0:
            faltantes += [(carta.id, carta.nome, abs(diferenca))]
    # retornar uma lista de tuplas: id, nome e quantidade
    return faltantes

def procurar_cartas_em_preconstruidos(id_cartas: list):
    preconstruidos = decks_preconstruidos()
    decks_contem = []
    for deck in preconstruidos:
        slot_deck = [slot.carta for slot in deck.composicao().get()]
        presentes = set(slot_deck) & set(id_cartas)
        if presentes:
            nomes_presentes = list(
                db.table('cartas')
                .where_in('id', list(presentes))
                .lists('nome')
            )
            decks_contem.append((deck.nome, nomes_presentes))
    return decks_contem

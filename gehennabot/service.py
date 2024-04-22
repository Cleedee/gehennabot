from datetime import date
from typing import List

from gehennabot import api

from gehennabot import sources
from gehennabot import util
from gehennabot.model import (
    Carta,
    Composicao,
    Deck,
    Entrada,
    ItemEntrada,
    ItemSaida,
    Saida,
    Usuario,
    db,
)


def legado_procurar_usuario(username: str) -> Usuario | None:
    return Usuario.where('username', '=', username).first()

def procurar_usuario(username):
    return api.procurar_usuario(username)

def legado_procurar_usuario_por_id(id) -> Usuario | None:
    return Usuario.find(id)

def procurar_usuario_por_id(id):
    return api.procurar_usuario_por_id(id)

def legado_procurar_usuarios():
    return Usuario.all()

def legado_estoque_da_carta(usuario, carta):
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

def estoque_da_carta(usuario, carta):
    return api.estoque_da_carta(usuario['username'], carta['id'])

def legado_total_estoque(username) -> int:
    usuario = procurar_usuario(username)
    total = 0
    total = (
        db.table('estoques').where('dono', '=', usuario['id']).sum('quantidade')
    )
    return total

def legado_procurar_carta(id: int) -> Carta:
    return Carta.find(id)

def procurar_carta(id: int):
    return api.procurar_carta_por_id(id)

def legado_procurar_carta_serializada(nome: str) -> dict:
    carta = Carta.where('nome', '=', nome).first()
    return carta.serialize() if carta else {}

def procurar_carta_serializada(nome: str) -> dict:
    carta = api.procurar_carta_por_nome(nome)
    return carta if carta else {}


def procurar_carta_por_nome(nome: str) -> dict:
    carta = api.procurar_carta_por_nome(nome)
    return carta if carta else {}


def legado_procurar_cartas_por_nome(nome: str) -> list[Carta]:
    return Carta.where('nome', 'like', f'%{nome}%').get()

def procurar_cartas_por_nome(nome: str) -> list[dict]:
    return api.procurar_cartas_por_nome(nome)

def todas_as_cartas() -> list[dict]:
    return api.procurar_cartas_todas()

def legado_todas_as_cartas() -> list[Carta]:
    return Carta.all()

def legado_estoques_por_carta(codigo) -> list[str]:
    carta = Carta.find(codigo)
    codigo_usuarios = [dono.username for dono in carta.donos]
    return codigo_usuarios


def legado_decks_por_usuario(username) -> list[Deck]:
    usuario = Usuario.where('username', '=', username).first()
    if usuario:
        decks = Deck.where('dono', '=', usuario.id).get()
        return decks
    return []


def legado_deck_por_id(id) -> Deck | None:
    return Deck.find(id)


def legado_decks_por_nome(username: str, nome_deck: str) -> list[Deck]:
    decks = legado_decks_por_usuario(username)
    return [deck for deck in decks if nome_deck in deck.nome]


def legado_decks_preconstruidos():
    return Deck.where('preconstruido', '=', 'T').get()


def legado_criar_copia_deck(deck_id):
    deck = legado_deck_por_id(deck_id)
    novo_deck = Deck()
    novo_deck.nome = deck.nome
    novo_deck.descricao = deck.descricao
    novo_deck.dono = deck.dono
    novo_deck.tipo = deck.tipo
    novo_deck.save()
    slots = legado_composicao_deck(deck.id)
    for slot in slots:
        c = Composicao()
        c.deck = novo_deck.id
        c.quantidade = slot.quantidade
        c.carta = slot.id
        c.save()
    return novo_deck.id


def legado_adicionar_cartas_ao_deck(deck_id: int, carta_id: int, quantidade: int):
    c = Composicao()
    c.quantidade = quantidade
    c.deck = deck_id
    c.carta = carta_id
    c.save()


def legado_composicao_deck(id: int) -> list[Composicao]:
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


def legado_composicoes_deck_por_id(id: int) -> list[Composicao]:
    return Composicao.where('deck', '=', id).get()


def legado_extrair_deck_da_internet(url, usuario) -> Deck:
    slots = sources.select_search_strategy(url)
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
            c.deck = novo_deck.id
            c.quantidade = int(slot.quantidade)
            c.carta = carta.id
            c.save()
        else:
            nao_encontradas += f'\n{slot.quantidade} x {slot.nome}'
            novo_deck.descricao = nao_encontradas
    composicao = legado_composicao_deck(novo_deck.id)
    nome = util.sugestao_nome_deck(composicao)
    novo_deck.nome = nome
    novo_deck.save()
    return novo_deck


def legado_entradas_por_usuario(usuario: Usuario):
    return Entrada.where('dono', '=', usuario.id).get()

def legado_saidas_por_usuario(usuario: Usuario):
    return Saida.where('dono', '=', usuario.id).get()


def legado_entrada_por_id(id: int) -> Entrada:
    return Entrada.find(id)


def legado_saida_por_id(id: int) -> Saida:
    return Saida.find(id)

def legado_itens_entrada_por_entrada_id(id: int) -> List[ItemEntrada]:
    return ItemEntrada.where('entrada','=', id).get()

def legado_itens_saida_por_saida_id(id: int) -> List[ItemSaida]:
    return ItemSaida.where('saida', '=', id).get()

def legado_detalhe_entrada(entrada_id) -> str:
    entrada = legado_entrada_por_id(entrada_id)
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


def legado_detalhe_saida(saida_id) -> str:
    saida = legado_saida_por_id(saida_id)
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


def legado_adicionar_deck_como_entrada(deck_id: int, username: str):
    with db.transaction():
        deck = legado_deck_por_id(deck_id)
        composicao = legado_composicao_deck(deck.id)
        usuario = legado_procurar_usuario(username)
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


def legado_cartas_que_faltam_para_o_deck(deck: Deck):
    faltantes = []
    usuario = legado_procurar_usuario_por_id(deck.dono)
    # trazer a composição do deck
    composicoes = legado_composicoes_deck_por_id(deck.id)
    # comparar cada slot com o estoque
    for composicao in composicoes:
        carta = legado_procurar_carta(composicao.carta)
        estoque = legado_estoque_da_carta(usuario, carta)
        diferenca = estoque - composicao.quantidade
        if diferenca < 0:
            faltantes += [(carta.id, carta.nome, abs(diferenca))]
    # retornar uma lista de tuplas: id, nome e quantidade
    return faltantes


def legado_procurar_cartas_em_preconstruidos(id_cartas: list):
    preconstruidos = legado_decks_preconstruidos()
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

from pyrogram import Client, filters, enums
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from dotenv import dotenv_values

import service
import util
from model import db

CARTAS_DE_CRIPTA = ['Vampire', 'Imbuid']

config = dotenv_values('.env')

print('Iniciando...')

usuarios = {
    'Cleedee': 'torcato',
    'igorcarmo': 'igorak',
    'lucasgolden': 'lucasgolden',
    'paulophi': 'vdeving',
    'igoxr': 'igoxr',
}

app = Client(
    'RutorsHandBot',
    api_id=config['API_ID'],
    api_hash=config['API_HASH'],
    bot_token=config['TOKEN_API'],
)


def representa_library(codigo_carta, usuario):
    carta = service.procurar_carta(codigo_carta)
    total_estoque = service.estoque_da_carta(usuario, carta)
    username_list = service.estoques_por_carta(carta.id)
    donos = ' '.join(username_list)
    texto = f"""
**Nome:** {carta.nome}\n
**Tipo:** {carta.tipo}\n
**Disciplina:** {carta.disciplinas}\n
**Texto:** {carta.descricao}\n
**No acervo de:** {donos}\n
**No meu acervo:** {total_estoque}
    """
    return texto


def representa_crypt(codigo_carta, usuario):
    carta = service.procurar_carta(codigo_carta)
    total_estoque = service.estoque_da_carta(usuario, carta)
    username_list = service.estoques_por_carta(carta.id)
    donos = ' '.join(username_list)
    texto = f"""
**Nome:** {carta.nome}\n
**Capacidade:** {carta.capacidade}\n
**Disciplina:** {carta.disciplinas}\n
**Seita:** {carta.seita}\n
**Texto:** {carta.descricao}\n
**No acervo de:** {donos}\n
**No meu acervo:** {total_estoque}
    """
    return texto


def colocar_titulo(titulo: str, texto: str) -> str:
    return f'**{titulo}**\n\n' + texto


@app.on_message(filters.command(['eu']))
async def eu_handler(_, message):
    username = message.from_user.username
    if username in usuarios:
        total = service.total_estoque(usuarios[username])
        await app.send_message(
            message.chat.id, 'Você tem {} cartas'.format(total)
        )
    else:
        await app.send_message(message.chat.id, 'Conta não encontrada.')


@app.on_message(filters.command(['carta']))
async def procuracarta_handler(_, message):
    nome = ' '.join(message.command[1:])
    carta = service.procurar_carta_serializada(nome)
    username = message.from_user.username
    if username not in usuarios:
        await app.send_message(message.chat.id, 'Conta não encontrada.')
    nick_usuario_gehenna = usuarios[username]
    usuario = service.procurar_usuario(nick_usuario_gehenna)
    if carta:
        texto = (
            representa_crypt(carta['id'], usuario)
            if carta['tipo'] in CARTAS_DE_CRIPTA
            else representa_library(carta['id'], usuario)
        )
        await app.send_message(
            message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
        )
    else:
        await app.send_message(message.chat.id, 'Carta não encontrada.')


@app.on_message(filters.command(['decks']))
async def decks_handler(_, message):
    username = message.from_user.username
    if username not in usuarios:
        await app.send_message(message.chat.id, 'Conta não encontrada.')
    decks = service.decks_por_usuario(usuarios[username])
    if decks:
        texto = '\n'.join([str(d.id) + ' - ' + d.nome for d in decks])
        texto = colocar_titulo('Decks Registrados', texto)
        await app.send_message(message.chat.id, texto)
    else:
        await app.send_message(message.chat.id, 'Decks não encontrados.')


@app.on_message(filters.command(['deck']))
async def deck_handler(_, message):
    if len(message.command) < 2:
        await app.send_message(message.chat.id, 'Informe o ID do deck.')
        return
    id = message.command[1]
    username = message.from_user.username
    if username not in usuarios:
        await app.send_message(message.chat.id, 'Conta não encontrada.')
        return
    deck = service.deck_por_id(id)
    if not deck:
        await app.send_message(message.chat.id, 'Deck não encontrado.')
    composicao = service.composicao_deck(id)
    texto = f'**Nome:** {deck.nome}\n'
    texto += f'**Descrição:**\n{deck.descricao}\n'
    texto += '\n'.join(
        [str(c.quantidade) + ' x ' + c.nome for c in composicao]
    )
    await app.send_message(message.chat.id, texto)


@app.on_message(filters.command(['falta']))
async def falta_no_handler(_, message):
    id = message.command[1]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    slots = service.composicao_deck(id)
    comparador = {}
    for slot in slots:
        carta = service.procurar_carta(slot.id)
        estoque = service.estoque_da_carta(usuario, carta)
        comparador[slot.id] = {
            'quantidade': slot.quantidade,
            'estoque': estoque,
            'nome': carta.nome,
        }
    em_falta = {}
    for id_carta in comparador.keys():
        diferenca = (
            comparador[id_carta]['quantidade']
            - comparador[id_carta]['estoque']
        )
        if diferenca > 0:
            em_falta[comparador[id_carta]['nome']] = diferenca
    texto = '\n'.join(
        [str(em_falta[carta]) + ' x ' + carta for carta in em_falta.keys()]
    )
    if em_falta:
        texto = colocar_titulo('Cartas que faltam para montar o deck', texto)
        await app.send_message(
            message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
        )

    else:
        await app.send_message(message.chat.id, 'Não falta nenhuma carta.')


@app.on_message(filters.command(['extrair']))
async def deck_from_url_handler(_, message):
    url = message.command[1]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    deck = service.extrair_deck_da_internet(url, usuario)
    if deck:
        await app.send_message(message.chat.id, f'{deck.nome} criado.')
    else:
        await app.send_message(
            message.chat.id, 'Nenhum deck encontrado nesta URL.'
        )


@app.on_message(filters.command(['onde']))
async def onde_encontrar_handler(_, message):
    deck_id = message.command[1]
    username = message.from_user.username
    preconstruidos = service.decks_preconstruidos()
    meu_deck = service.deck_por_id(deck_id)
    cartas_meu_deck = [slot.carta for slot in meu_deck.composicao().get()]
    decks_contem = []
    for deck in preconstruidos:
        slot_deck = [slot.carta for slot in deck.composicao().get()]
        presentes = set(slot_deck) & set(cartas_meu_deck)
        if presentes:
            nomes_presentes = list(
                db.table('cartas')
                .where_in('id', list(presentes))
                .lists('nome')
            )
            decks_contem.append((deck.nome, nomes_presentes))
    texto = '\n'.join(
        [
            f'**{item[0]}**' + '\n\t\t' + '\n\t\t'.join(item[1])
            for item in decks_contem
        ]
    )
    texto = colocar_titulo(
        'Preconstruídos onde as cartas são encontradas', texto
    )
    await app.send_message(message.chat.id, texto)

@app.on_message(filters.command(['ondefaltantes']))
async def mostrar_faltantes_preconstruidos_handler(_, message):
    if len(message.command) < 2:
        await app.send_message(message.chat.id, 'Informe o ID do deck.')
        return
    deck_id = message.command[1]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    preconstruidos = service.decks_preconstruidos()
    meu_deck = service.deck_por_id(deck_id)
    if meu_deck.dono != usuario.id:
        await app.send_message(message.chat.id, 'Deck não encontrado.')
        return
    faltantes = service.cartas_que_faltam_para_o_deck(meu_deck)
    id_cartas = [id for (id, _, _) in faltantes]
    pre_e_cartas = service.procurar_cartas_em_preconstruidos(id_cartas)
    texto = '\n'.join(
        [
            f'**{item[0]}**' + '\n\t\t' + '\n\t\t'.join(item[1])
            for item in pre_e_cartas
        ]
    )
    texto = colocar_titulo(
        f'Você pode encontrar as cartas que faltam a seguir para o {meu_deck.nome}', texto
    )
    await app.send_message(message.chat.id, texto)

@app.on_message(filters.command(['entradas']))
async def entradas_handler(_, message):
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    entradas = service.entradas_por_usuario(usuario)
    texto = '\n'.join(
        [f'{entrada.id} - {entrada.origem}' for entrada in entradas]
    )
    texto = colocar_titulo('Movimentações de Entradas de Cartas', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_message(filters.command(['detalhe_entrada']))
async def detalhe_entrada(_, message):
    entrada_id = message.command[1]
    entrada = service.entrada_por_id(entrada_id)
    texto = service.detalhe_entrada(entrada_id)
    texto = colocar_titulo(f'Detalhes da Movimentação de Entrada {entrada.origem}', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_message(filters.command(['saidas']))
async def saidas_handler(_, message):
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    saidas = service.saidas_por_usuario(usuario)
    texto = '\n'.join(
        [f'{saida.id} - {saida.descricao}' for saida in saidas]
    )
    texto = colocar_titulo('Movimentações de Saídas de Cartas', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_message(filters.command(['detalhe_saida']))
async def detalhe_saida(_, message):
    saida_id = message.command[1]
    saida = service.saida_por_id(saida_id)
    texto = service.detalhe_saida(saida_id)
    texto = colocar_titulo(f'Detalhes da Movimentação de Saida {saida.descricao}', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command(['sugerir_nome_deck']))
async def sugerir_nome_deck_handler(_, message):
    if len(message.command) < 2:
        await app.send_message(message.chat.id, 'Informe o ID do deck.')
        return
    deck_id = message.command[1]
    composicao = service.composicao_deck(deck_id)
    nome_sugerido = util.sugestao_nome_deck(composicao)
    await app.send_message(
        message.chat.id, nome_sugerido, parse_mode=enums.ParseMode.MARKDOWN
    )


app.run()
print('Encerrando...')

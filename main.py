from pyrogram import Client, filters, enums
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from dotenv import dotenv_values

import service

CARTAS_DE_CRIPTA = ['Vampire', 'Imbuid']
config = dotenv_values('.env')

print('Iniciando...')

usuarios = {
    'Cleedee': 'torcato',
    'igorcarmo': 'igorak',
    'lucasgolden': 'lucasgolden',
    'paulophi': 'vdeving',
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


@app.on_message(filters.command(['eu']))
async def eu_handler(client, message):
    username = message.from_user.username
    if username in usuarios:
        total = service.total_estoque(usuarios[username])
        await app.send_message(
            message.chat.id, 'Você tem {} cartas'.format(total)
        )
    else:
        await app.send_message(message.chat.id, 'Conta não encontrada.')


@app.on_message(filters.command(['carta']))
async def procuracarta_handler(client, message):
    nome = ' '.join(message.command[1:])
    carta = service.procurar_carta_serializada(nome)
    username = message.from_user.username
    nick_usuario_gehenna = usuarios[username]
    usuario = service.procurar_usuario(nick_usuario_gehenna)
    if carta:
        print(carta)
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
async def decks_handler(client, message):
    username = message.from_user.username
    decks = service.decks_por_usuario(usuarios[username])
    if decks:
        texto = '\n'.join([str(d.id) + ' - ' + d.nome for d in decks])
        await app.send_message(message.chat.id, texto)
    else:
        await app.send_message(message.chat.id, 'Decks não encontrados.')


@app.on_message(filters.command(['deck']))
async def deck_handler(client, message):
    id = message.command[1:]
    username = message.from_user.username
    composicao = service.composicao_deck(id, usuarios[username])
    texto = '\n'.join([str(c.quantidade) + ' x ' + c.nome for c in composicao])
    await app.send_message(message.chat.id, texto)


@app.on_message(filters.command(['falta']))
async def falta_no_handler(client, message):
    id = message.command[1:]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    slots = service.composicao_deck(id, usuarios[username])
    cartas_id = [slot.id for slot in slots]
    print(cartas_id)
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
        diferenca = comparador[id_carta]['quantidade'] - comparador[id_carta]['estoque']
        if diferenca > 0:
            em_falta[comparador[id_carta]['nome']] = diferenca
    texto = '\n'.join(
        [str(em_falta[carta]) + ' x ' + carta for carta in em_falta.keys()]
    )
    await app.send_message(message.chat.id, texto)


app.run()
print('Encerrando...')

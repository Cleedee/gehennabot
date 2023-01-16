from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from dotenv import dotenv_values

import service

config = dotenv_values(".env")

print('Iniciando...')

usuarios = {
    'Cleedee': 'torcato',
    'igorcarmo': 'igorak'
}

app = Client(
    "RutorsHandBot", 
    api_id=config['API_ID'], 
    api_hash=config['API_HASH'], 
    bot_token=config['TOKEN_API'])

@app.on_message(filters.command(['eu']))
async def eu_handler(client, message):
    username = message.from_user.username
    if username in usuarios: 
        total = service.total_estoque(username)
        await app.send_message(message.chat.id,'Você tem {} cartas'.format(total))
    else:
        await app.send_message(message.chat.id,'Conta não encontrada.')

@app.on_message(filters.command(['procuracarta']))
async def procuracarta_handler(client, message):
    nome = ' '.join(message.command[1:])
    carta = service.procurar_carta(nome)
    if carta:
        teclado = ReplyKeyboardMarkup(
            [
                ['Estoques', 'Meu Estoque',]
            ],
            resize_keyboard = True,
            one_time_keyboard = True
        )
        await app.send_message(
            message.chat.id, 
            carta['descricao'],
            reply_markup = teclado,
            )
    else:
        await app.send_message(message.chat.id,'Carta não encontrada.')


app.run()
print('Encerrando...')
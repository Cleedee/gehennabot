from typing import Dict, List
import service
import util
from dotenv import dotenv_values
from pyrogram import Client, enums, filters

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
    users = service.procurar_donos_da_carta(carta['id'])
    donos = ' '.join([ u['username'] for u in users ])
    texto = f"""
**Nome:** {carta['name']} ({codigo_carta})\n
**Tipo:** {carta['tipo']}\n
**Disciplina:** {carta['disciplines']}\n
**Texto:** {carta['text']}\n
**No acervo de:** {donos}\n
**No meu acervo:** {total_estoque}
    """
    return texto


def representa_crypt(codigo_carta, usuario):
    carta = service.procurar_carta(codigo_carta)
    total_estoque = service.estoque_da_carta(usuario, carta)
    users = service.procurar_donos_da_carta(carta['id'])
    donos = ' '.join([ u['username'] for u in users ])
    texto = f"""
**Nome:** {carta['name']} ({codigo_carta})\n
**Capacidade:** {carta['capacity']}\n
**Disciplina:** {carta['disciplines']}\n
**Seita:** {carta['sect']}\n
**Texto:** {carta['text']}\n
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
    carta = service.procurar_carta_por_nome(nome)
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
        # tenta ver se na mensagem vem um ID
        if nome.isdigit():
            carta_id = int(nome)
            carta = service.procurar_carta(carta_id)
            if carta:
                texto = (
                    representa_crypt(carta['id'], usuario)
                    if carta['tipo'] in CARTAS_DE_CRIPTA
                    else representa_library(carta['id'], usuario)
                )
                await app.send_message(
                    message.chat.id, 
                    texto, 
                    parse_mode=enums.ParseMode.MARKDOWN)
        else:
            await app.send_message(message.chat.id, 'Carta não encontrada.')


@app.on_message(filters.command(['decks']))
async def decks_handler(_, message):
    username = message.from_user.username
    if username not in usuarios:
        await app.send_message(message.chat.id, 'Conta não encontrada.')
    decks = service.decks_por_usuario(usuarios[username])
    if decks:
        chunks = list(util.divide_chunks(decks, 20))
        for baralhos in chunks:
            texto = '\n'.join([str(d['id']) + ' - ' + d['name'] for d in baralhos])
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
    slots = service.slots_por_deck(id)
    texto = f"**Nome:** {deck['name']}\n"
    texto += f"**Descrição:**\n{deck['description']}\n"
    texto += '\n'.join(
        [str(s['quantity']) + ' x ' + s['card']['name'] for s in slots]
    )
    await app.send_message(message.chat.id, texto)


@app.on_message(filters.command(['falta']))
async def falta_no_handler(_, message):
    id = message.command[1]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    slots = service.slots_por_deck(id)
    comparador = {}
    for slot in slots:
        carta = service.procurar_carta(slot['card_id'])
        estoque = service.estoque_da_carta(usuario, carta)
        comparador[slot['id']] = {
            'quantidade': slot['quantity'],
            'estoque': estoque,
            'nome': carta['name'],
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
    deck, slots = service.extrair_deck_da_internet(url, usuario)
    deck = service.cadastrar_deck(deck, slots)
    if deck:
        await app.send_message(message.chat.id, f'{deck["name"]} criado com id {deck["id"]}.')
    else:
        await app.send_message(
            message.chat.id, 'Nenhum deck encontrado nesta URL.'
        )


@app.on_message(filters.command(['onde']))
async def onde_encontrar_handler(_, message):
    deck_id = message.command[1]
    preconstruidos = service.decks_preconstruidos()
    meu_deck = service.deck_por_id(deck_id)
    slots = service.slots_por_deck(meu_deck['id'])
    cartas_meu_deck = [slot['card']['id'] for slot in slots]
    #print(cartas_meu_deck)
    decks_contem = []
    for deck in preconstruidos:
        slots_deck = service.slots_por_deck(deck['id'])
        slot_deck = [slot['card']['id'] for slot in slots_deck]
        presentes = set(slot_deck) & set(cartas_meu_deck)
        #print('PRESENTES', presentes)
        if presentes:
            nomes_presentes = [ carta['name'] for carta in service.procurar_cartas_por_ids(presentes)]
            decks_contem.append((deck['name'], nomes_presentes))
    chunks = list(util.divide_chunks(decks_contem, 10))
    texto = colocar_titulo(
        'Preconstruídos onde as cartas são encontradas', ''
    )
    await app.send_message(message.chat.id, texto)
    for nomes in chunks:
        texto = '\n'.join(
            [
                f'**{item[0]}**' + '\n\t\t' + '\n\t\t'.join(item[1])
                for item in nomes
            ]
        )
        print(texto)
        await app.send_message(message.chat.id, texto)


@app.on_message(filters.command(['onde_faltantes']))
async def mostrar_faltantes_preconstruidos_handler(_, message):
    if len(message.command) < 2:
        await app.send_message(message.chat.id, 'Informe o ID do deck.')
        return
    deck_id = message.command[1]
    username = message.from_user.username
    usuario = service.procurar_usuario(usuarios[username])
    meu_deck = service.deck_por_id(deck_id)
    if meu_deck is None:
        await app.send_message(message.chat.id, 'Deck não encontrado.')
        return
    if meu_deck['owner_id'] != usuario['id']:
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
        (
            'Você pode encontrar as cartas que'
            f'faltam a seguir para o {meu_deck.nome}'
        ),
        texto,
    )
    await app.send_message(message.chat.id, texto)


@app.on_message(filters.command(['entradas']))
async def entradas_handler(_, message):
    username = message.from_user.username
    entradas = service.entradas_por_usuario(usuarios[username])
    texto = '\n'.join(
        [f"{entrada['id']} - {entrada['name']}" for entrada in entradas]
    )
    texto = colocar_titulo('Movimentações de Entradas de Cartas', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command(['detalhe_entrada', 'detalhe_saida']))
async def detalhe_entrada(_, message):
    movimentacao_id = message.command[1]
    movimentacao = service.movimentacao_por_id(movimentacao_id)
    if not movimentacao:
        await app.send_message(message.chat.id, 'Movimentação não encontrada.')
        return
    itens = service.itens_por_movimentacao(movimentacao_id)
    texto = '\n'.join(
        [f"{item['quantity']}x {item['card']['name']}" for item in itens  ]
    )
    texto = colocar_titulo(
        f"Detalhes da Movimentação de Entrada {movimentacao['name']}", texto
    )
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command(['saidas']))
async def saidas_handler(_, message):
    username = message.from_user.username
    saidas = service.saidas_por_usuario(usuarios[username])
    texto = '\n'.join([f"{saida['id']} - {saida['name']}" for saida in saidas])
    texto = colocar_titulo('Movimentações de Saídas de Cartas', texto)
    await app.send_message(
        message.chat.id, texto, parse_mode=enums.ParseMode.MARKDOWN
    )

# TODO reimplementar
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

@app.on_message(filters.command(['renomear']))
async def renomear_handler(_, message):
    if len(message.command) < 2:
        await app.send_message(message.chat.id, 'Informe o ID do deck.')
        return
    id = message.command[1]
    nome = ' '.join(message.command[2:])
    username = message.from_user.username
    if username not in usuarios:
        await app.send_message(message.chat.id, 'Conta não encontrada.')
        return
    deck = service.deck_por_id(id)
    if not deck:
        await app.send_message(message.chat.id, 'Deck não encontrado.')
        return
    deck['name'] = nome
    service.atualizar_deck(deck)
    await app.send_message(message.chat.id, 'Deck atualizado.')

@app.on_message(filters.command(['cartas']))
async def cartas_handler(_, message):
    nome = ' '.join(message.command[1:])
    print(nome)
    cartas: List[Dict] = service.procurar_cartas_por_nome(nome)
    if cartas:
        texto = '\n'.join(
            [f"{carta['id']} - {carta['name']} ({carta['tipo']})" for carta in cartas]
        )
        await app.send_message(message.chat.id, texto)
    else:
        await app.send_message(message.chat.id, 'Nenhuma carta encontrada.')

    


app.run()
print('Encerrando...')

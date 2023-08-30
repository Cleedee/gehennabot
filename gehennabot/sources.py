from collections import namedtuple
from typing import List
import json

import requests

from gehennabot import config

URL_API_TWD = 'https://vdb.im/api/twd/'
URL_API_PDA = 'https://vdb.im/api/pda/'
URL_API_DECK = 'https://vdb.im/api/deck/'

Slot = namedtuple('Slot', 'quantidade nome')


def select_search_strategy(url: str) -> List[Slot]:
    if 'vdb.im' in url:
        return slots_from_vdb(url)
    if 'https://vtesdecks.com/' in url:
        print('Aqui')
        return slots_from_vtescards(url)
    return []


def slots_from_vtescards(url: str) -> List[Slot]:
    deck_id = url.split('deck/')[1]
    r = requests.get(
        'https://api.vtesdecks.com/1.0/decks/'
        + deck_id
        + '/export?type=LACKEY'
    )
    if r.status_code != 200:
        return []
    texto = r.text
    lines = [line for line in texto.split('\n') if '\t' in line]
    slots = [Slot(*line.split('\t')) for line in lines]
    return slots


def slots_from_vdb(url: str) -> List[Slot]:
    deckid = url.replace('https://vdb.im/decks/', '')
    url = URL_API_DECK + deckid
    r = requests.get(url)
    if r.status_code != 200:
        return []
    cards = r.json().get('cards')
    # TODO pegar o nome das cartas nos arquivos json
    data_cards = data_crypt  = data_library = {}
    with open(config.CRYPT_FILE_PATH) as file:
        data_crypt = json.load(file)
    data_cards.update(data_crypt)
    with open(config.LIBRARY_FILE_PATH) as file:
        data_library = json.load(file)
    data_cards.update(data_library)
    slots = []
    for key in cards.keys():
        card = data_cards[key]
        slot = Slot(cards[key], card['Name'])
        slots.append(slot)
    return slots


def slots_from_amaranth(url: str) -> list[Slot]:
    return []

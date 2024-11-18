from collections import namedtuple
from typing import Dict, List
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
        print('Deck não encontrado.')
        return {}
    texto = r.text
    lines = [line for line in texto.split('\n') if '\t' in line]
    slots = [Slot(*line.split('\t')) for line in lines]
    return slots


def slots_from_vdb(url: str) -> Dict:
    deckid = url.replace('https://vdb.im/decks/', '')
    url = URL_API_DECK + deckid
    r = requests.get(url)
    if r.status_code != 200:
        print('Deck não encontrado.')
        return {}
    cards = r.json().get('cards')
    return cards 


def slots_from_amaranth(url: str) -> list[Slot]:
    return []

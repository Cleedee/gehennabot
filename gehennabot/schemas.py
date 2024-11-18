from typing import NamedTuple
from collections import namedtuple

#class Item(NamedTuple):
#    card_id: int
#    moviment_id: int
#    quantity: int
#    code: int

Item = namedtuple('Item', 'card_id moviment_id quantity code')

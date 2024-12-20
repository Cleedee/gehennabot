from collections import namedtuple
from dataclasses import dataclass
from datetime import date, datetime

#class Item(NamedTuple):
#    card_id: int
#    moviment_id: int
#    quantity: int
#    code: int

Item = namedtuple('Item', 'card_id moviment_id quantity code')

@dataclass()
class Deck:
    name: str
    description: str
    tipo: str
    owner_id: int
    creator: str = ''
    player: str = ''
    created: date | None = None
    updated: datetime | None = None
    preconstructed: bool = False
    code: int = 0


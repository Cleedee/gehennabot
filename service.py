from model import Usuario, Carta, Estoque, Deck, Composicao, db
from model import Entrada, Saida, ItemEntrada, ItemSaida

def procurar_usuario(username):
    return Usuario.where('username','=', username).first()

def estoque_da_carta(usuario, carta):
    soma_entradas = db.table('detalhes')\
        .join('entradas','entradas.id','=','detalhes.entrada')\
        .where('detalhes.carta','=',carta.id)\
        .where('entradas.dono','=',usuario.id)\
        .sum('detalhes.quantidade')
    soma_saidas = db.table('itens_saida')\
        .join('saidas','saidas.id','=','itens_saida.saida')\
        .where('itens_saida.carta','=',carta.id)\
        .where('saidas.dono','=',usuario.id)\
        .sum('itens_saida.quantidade')
    soma_entradas = soma_entradas if soma_entradas else 0
    soma_saidas = soma_saidas if soma_saidas else 0
    total = soma_entradas - soma_saidas
    return total


def total_estoque(username):
    usuario = procurar_usuario(username)
    total = 0
    total = db.table('estoques') \
        .where('dono','=',usuario.id) \
        .sum('quantidade')
    return total

def procurar_carta(codigo):
    return Carta.find(codigo)

def procurar_carta_serializada(nome):
    carta = Carta.where('nome','=',nome).first()
    return carta.serialize() if carta else {}

def estoques_por_carta(codigo):
    carta = Carta.find(codigo)
    codigo_usuarios = [ dono.username for dono in carta.donos ]
    return codigo_usuarios

def decks_por_usuario(username):
    usuario = Usuario.where('username','=', username).first()
    if usuario:
        decks = Deck.where('dono','=',usuario.id).get()
        return decks
    return []

def deck_por_id(id, username):
    usuario = procurar_usuario(username)
    deck = Deck.find(id)
    if deck.dono == usuario.id:
        return deck
    return None

def composicao_deck(id, username):
    usuario = procurar_usuario(username)
    composicao = db.table('composicao') \
        .join('cartas','composicao.carta','=','cartas.id') \
        .select('composicao.quantidade', 'cartas.nome') \
        .where('composicao.deck','=',id) \
        .get()    
    return composicao
from model import Usuario, Carta, Estoque, db

def total_estoque(username):
    total = 0
    total = db.table('estoques') \
        .join('auth_user','estoques.dono','=','auth_user.id') \
        .select('auth_user','username','=',username) \
        .count()
    return total

def procurar_carta(nome):
    carta = Carta.where('nome','=',nome).first()
    return carta.serialize() if carta else {}

def estoques_por_carta(codigo):
    estoques = Estoque.where('carta', '=', codigo).get()
    codigo_usuarios = [ e.dono.id for e in estoques ]
    return codigo_usuarios

import typer

from gehennabot.service import (
    adicionar_deck_como_entrada, 
    decks_preconstruidos, 
    procurar_usuarios,
    procurar_cartas_por_nome,
    decks_por_nome,
    adicionar_cartas_ao_deck,
    deck_por_id,
    cartas_que_faltam_para_o_deck,
    procurar_cartas_em_preconstruidos
)

app = typer.Typer()

@app.command()
def preconstruidos():
    lista = decks_preconstruidos()
    for deck in lista:
        print(deck.id, deck.nome)

@app.command()
def usuarios():
    lista = procurar_usuarios()
    for usuario in lista:
        print(usuario.username)

@app.command()
def adicionar_precon(deck_id: int, dono: str):
    entrada = adicionar_deck_como_entrada(deck_id, dono)
    if entrada:
        print('Nova entrada incluída.')
    else:
        print('Deck preconstruído não pôde ser adicionado.')

@app.command()
def procura_carta(nome: str):
    lista = procurar_cartas_por_nome(nome)
    for carta in lista:
        print(carta.id, carta.nome)

@app.command()
def decks(nome: str, username='torcato'):
    lista = decks_por_nome(username, nome)
    for deck in lista:
        print(deck.id, deck.nome)

@app.command()
def adicionar(deck_id: int, carta_id: int, quantidade: int):
    adicionar_cartas_ao_deck(deck_id, carta_id, quantidade)
    print('Cartas adicionadas.')

@app.command()
def falta(deck_id: int):
    deck = deck_por_id(deck_id)
    faltantes = cartas_que_faltam_para_o_deck(deck)
    for id, nome, quantidade in faltantes:
        print(quantidade, f"({id}) {nome}")

@app.command()
def falta_e_procura(deck_id: int):
    deck = deck_por_id(deck_id)
    faltantes = cartas_que_faltam_para_o_deck(deck)
    decks = procurar_cartas_em_preconstruidos([id for (id, _, _) in faltantes])
    for deck in decks:
        print(deck[0])
        for carta in deck[1]:
            print('    ',carta)

def preconstruido_como_saida(deck_id, dono_id):
    pass

if __name__ == "__main__":
    app()

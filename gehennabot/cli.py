import typer

from gehennabot.service import (
    adicionar_deck_como_entrada, 
    decks_preconstruidos, 
    procurar_usuarios,
    procurar_cartas_por_nome,
    decks_por_nome,
    adicionar_cartas_ao_deck
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

def preconstruido_como_saida(deck_id, dono_id):
    pass

if __name__ == "__main__":
    app()

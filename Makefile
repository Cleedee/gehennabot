procura-carta:
	poetry run python gehennabot/cli.py procura-carta ${nome}
help:
	poetry run python gehennabot/cli.py --help
adiciona-carta:
	poetry run python gehennabot/cli.py adicionar ${deck} ${card} ${quantidade}
baixar-internet:
	poetry run python gehennabot/cli.py baixar-internet ${deckid} ${username}
falta:
	poetry run python gehennabot/cli.py falta ${deckid}
falta-procura:
	poetry run python gehennabot/cli.py falta-e-procura ${deckid}
decks:
	poetry run python gehennabot/cli.py decks ${name}
deck-vdb:
	poetry run python gehennabot/cli.py deck-vdb ${deckid}
servidor:
	poetry run python gehennabot/main.py

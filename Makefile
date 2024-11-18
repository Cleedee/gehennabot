procura-carta:
	poetry run python gehennabot/cli.py procura-carta ${nome}
procura-carta-id:
	poetry run python gehennabot/cli.py procura-carta-id ${id}
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
usuarios:
	poetry run python gehennabot/cli.py usuarios
movimentacoes:
	poetry run python gehennabot/cli.py gehenna-api-create-moviment ${username}
itens:
	poetry run python gehennabot/cli.py gehenna-api-create-item ${username}
import-decks:
	poetry run python gehennabot/cli.py gehenna-api-create-decks ${username}
import-slots:
	poetry run python gehennabot/cli.py gehenna-api-create-slots ${username}
import-deck:
	poetry run python gehennabot/cli.py gehenna-api-create-deck ${code}
import-slots-deck:	
	poetry run python gehennabot/cli.py gehenna-api-create-slots-deck ${code}
import-total-decks:
	poetry run python gehennabot/cli.py total-decks ${username}
adicionar-precon:
	poetry run python gehennabot/cli.py adicionar-precon ${deck_id} ${username}

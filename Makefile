.PHONY: lint format

env:
	uv sync

lint:
	uv run ruff . && uv run blue --check . --diff

format:
	uv run blue . && uv run isort .

procura-carta:
	uv run python -m gehennabot.cli procura-carta $(nome)

procura-carta-id:
	uv run python -m gehennabot.cli procura-carta-id $(id)

help:
	uv run python -m gehennabot.cli --help

adiciona-carta:
	uv run python -m gehennabot.cli adicionar $(deck) $(card) $(quantidade)

baixar-internet:
	uv run python -m gehennabot.cli baixar-internet $(deckid) $(username)

falta:
	uv run python -m gehennabot.cli falta $(deckid)

falta-procura:
	uv run python -m gehennabot.cli falta-e-procura $(deckid)

decks:
	uv run python -m gehennabot.cli decks $(name)

deck-vdb:
	uv run python -m gehennabot.cli deck-vdb $(deckid)

apagar-deck:
	uv run python -m gehennabot.cli apagar-deck $(id)

server:
	cd gehennabot && uv run python -m gehennabot.main

usuarios:
	uv run python -m gehennabot.cli usuarios

movimentacoes:
	uv run python -m gehennabot.cli gehenna-api-create-moviment $(username)

itens:
	uv run python -m gehennabot.cli gehenna-api-create-item $(username)

import-decks:
	uv run python -m gehennabot.cli gehenna-api-create-decks $(username)

import-slots:
	uv run python -m gehennabot.cli gehenna-api-create-slots $(username)

import-deck:
	uv run python -m gehennabot.cli gehenna-api-create-deck $(code)

import-slots-deck:
	uv run python -m gehennabot.cli gehenna-api-create-slots-deck $(code)

import-total-decks:
	uv run python -m gehennabot.cli total-decks $(username)

adicionar-precon:
	uv run python -m gehennabot.cli adicionar-precon $(deck_id) $(username)

preconstruidos:
	uv run python -m gehennabot.cli preconstruidos
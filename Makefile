procura-carta:
	poetry run python gehennabot/cli.py procura-carta ${nome}
help:
	poetry run python gehennabot/cli.py --help
adiciona-carta:
	poetry run python gehennabot/cli.py adicionar ${deck} ${card} ${quantidade}
	

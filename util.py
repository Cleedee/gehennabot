from model import Composicao, GRUPOS

def sugestao_nome_deck(composicoes: list[Composicao]):
    # adicione o principal vampiro
    # adicione os grupos da cripta
    grupos = []
    for slot in composicoes:
        grupo = slot.grupo
        if grupo not in grupos and slot.tipo == 'Vampire':
            grupos += [grupo]
    # adicione a principal disciplina
    # adicione Voto se tem cartas de voto
    return '/'.join(map(str, grupos))

from model import Composicao

def sugestao_nome_deck(composicoes: list[Composicao]):
    # adicione o clã principal
    cripta = []
    # adicione o principal vampiro
    # adicione os grupos da cripta
    grupos = []
    for slot in composicoes:
        grupo = slot.grupo
        if grupo not in grupos and slot.tipo == 'Vampire':
            grupos += [grupo]
        if slot.tipo == 'Vampire':
            cripta += slot.quantidade * [ slot.clan ]
    grupos.sort()
    grupos_cripta = '/'.join(map(str, grupos))
    # adicione a principal disciplina
    # adicione Voto se tem cartas de voto
    slots_cripta = {}
    for vampiro in cripta:
        if vampiro in slots_cripta:
            slots_cripta[vampiro] += 1
        else:
            slots_cripta[vampiro] = 1
    vampiros_ordenados_por_quantidade = sorted(slots_cripta.items(), key=lambda x: x[1], reverse=True)
    clan_mais_numeroso = vampiros_ordenados_por_quantidade[0][0]
    return ' '.join([clan_mais_numeroso, grupos_cripta])

from model import Composicao


def _quantifica_cartas(baralho):
    slots = {}
    for nome in baralho:
        if nome in slots:
            slots[nome] += 1
        else:
            slots[nome] = 1
    return slots


def _ordena_por_quantidade(slots):
    return sorted(slots.items(), key=lambda x: x[1], reverse=True)


def _quantidade_carta_mais_comum(slots):
    res = _ordena_por_quantidade(slots)
    return res[0][1]


def _carta_mais_comum(slots):
    por_quantidade = _ordena_por_quantidade(slots)
    return por_quantidade[0][0]


def sugestao_nome_deck(composicoes: list[Composicao]):
    cripta = []
    nomes_vampiros = []
    grupos = []
    numero_cartas_voto = 0
    partes = []
    # obter os valores
    for slot in composicoes:
        grupo = slot.grupo
        if grupo and grupo not in grupos and slot.tipo == 'Vampire':
            grupos += [grupo]
        if slot.tipo == 'Vampire':
            cripta += slot.quantidade * [slot.clan]
            nomes_vampiros += slot.quantidade * [slot.nome]
        if slot.tipo == 'Political Action':
            numero_cartas_voto += slot.quantidade
    # agindo sobre os valores para extrair os grupos
    grupos.sort()
    grupos_cripta = 'G' + '/'.join(map(str, grupos))
    partes = [grupos_cripta] + partes
    # agindo sobre os valores para extrair os clãs
    slots_cripta = {}
    for vampiro in cripta:
        if vampiro in slots_cripta:
            slots_cripta[vampiro] += 1
        else:
            slots_cripta[vampiro] = 1
    vampiros_ordenados_por_quantidade = sorted(
        slots_cripta.items(), key=lambda x: x[1], reverse=True
    )
    clan_mais_numeroso = vampiros_ordenados_por_quantidade[0][0]
    partes.append(clan_mais_numeroso)
    # agindo sobre os valores para extrair os vampiros
    slots_nomes = _quantifica_cartas(nomes_vampiros)
    vampiro_mais_numeroso = _carta_mais_comum(slots_nomes)
    quantidade_do_mais_numeroso = _quantidade_carta_mais_comum(slots_nomes)
    if quantidade_do_mais_numeroso > 3:
        partes.append(vampiro_mais_numeroso)
    if numero_cartas_voto > 8:
        partes.append('Voto')
    return ' '.join(partes)

import requests

# ——————————————————————————
# AUTENTICAÇÃO E CONFIGURAÇÃO
# ——————————————————————————
API_KEY = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = 'CqZynf3b'
LIST_NAME = 'Planejamento'
CARD_NAME = '📘 Eixo Temático 3 – Sistemas Operacionais e Redes (Checklist Estruturado)'

# ——————————————————————————
# CHECKLIST FORMATADO
# ——————————————————————————
checklist_items = [
    "3 Sistemas Operacionais.",
    "3.1 Conceitos básicos: funções e estruturas de sistemas operacionais.",
    "3.2 Gerenciamento de processos: escalonamento do processador, programação concorrente, deadlock, comunicação e sincronização.",
    "3.3 Gerenciamento de memória: partições, realocação, memória virtual, swapping.",
    "3.4 Sistemas de arquivos.",

    "4 Redes de Computadores.",
    "4.1 Conceitos básicos de redes de computadores e Internet.",

    "4.2 Camadas de protocolos e serviços:",
    "4.2.1 Camada Física: características do meio de transmissão, técnicas de transmissão.",
    "4.2.2 Camada de Aplicação: principais protocolos.",
    "4.2.3 Camada de Transporte: serviços, protocolos TCP e UDP, princípios do controle de congestionamento.",
    "4.2.4 Camada de Rede: protocolos IPv4 e IPv6, algoritmos de roteamento.",
    "4.2.5 Camada de Enlace e redes locais: serviços oferecidos, protocolos de acesso múltiplo, endereçamento na camada de enlace.",

    "4.3 Redes Ethernet.",
    "4.4 Redes sem fio.",
    "4.5 Redes móveis.",
    "4.6 Princípios da Gerência de Redes."
]


# ——————————————————————————
# FUNÇÕES AUXILIARES
# ——————————————————————————
def get_list_id(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {'key': API_KEY, 'token': TOKEN}
    r = requests.get(url, params=params)
    for lista in r.json():
        if lista['name'].lower() == list_name.lower():
            return lista['id']
    raise Exception(f"Lista '{list_name}' não encontrada.")


def create_card(list_id, name):
    url = "https://api.trello.com/1/cards"
    params = {'key': API_KEY, 'token': TOKEN, 'idList': list_id, 'name': name}
    r = requests.post(url, params=params)
    return r.json()['id']


def add_checklist(card_id, checklist_name, items):
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    params = {'key': API_KEY, 'token': TOKEN, 'name': checklist_name}
    checklist = requests.post(url, params=params).json()
    for item in items:
        item_url = f"https://api.trello.com/1/checklists/{checklist['id']}/checkItems"
        item_params = {'key': API_KEY, 'token': TOKEN, 'name': item, 'checked': 'false'}
        requests.post(item_url, params=item_params)


# ——————————————————————————
# EXECUÇÃO
# ——————————————————————————
list_id = get_list_id(BOARD_ID, LIST_NAME)
card_id = create_card(list_id, CARD_NAME)
add_checklist(card_id, "Checklist", checklist_items)

print("✅ Card com checklist do Eixo 3 criado com sucesso!")

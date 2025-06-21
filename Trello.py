import requests

# ——————————————————————————
# AUTENTICAÇÃO E CONFIGURAÇÃO
# ——————————————————————————
API_KEY = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = 'CqZynf3b'  # NOVO QUADRO
LIST_NAME = 'Planejamento'
CARD_NAME = '📘 Eixo Temático 2 – POLÍTICAS PÚBLICAS (Checklist Estruturado)'

# ——————————————————————————
# CHECKLIST NO ESTILO DA IMAGEM
# ——————————————————————————
checklist_items = [
    "1 O processo de elaboração de políticas.",
    "1.1 O papel do Estado.",
    "1.2 A burocracia e o Estado.",
    "1.3 Poder, racionalidade e tomada de decisões.",
    "1.4 O papel da burocracia e a discricionariedade no processo de formulação e implementação de políticas públicas.",

    "2 Implementação de políticas públicas: problemas, dilemas e desafios.",
    "2.1 Arranjos institucionais para implementação de políticas públicas.",

    "3 Avaliação de políticas públicas.",
    "3.1 Principais componentes do processo de avaliação.",
    "3.2 Custo-benefício, escala, efetividade, impacto das políticas públicas.",
    "3.3 Principais diretrizes da formulação, implementação e avaliação de políticas públicas.",

    "4 Políticas de ciência, tecnologia e inovação.",
    "4.1 Marco Legal de CT&I (Lei nº 13.243/2016).",
    "4.2 Política e Estratégia Nacional de CT&I.",
    "4.3 Política Nacional de Inovação.",

    "5 Políticas de Governo Digital.",
    "5.1 Lei nº 14.129/2021 – Governo Digital.",
    "5.2 Marco Civil da Internet – Lei nº 12.965/2014 e alterações.",
    "5.3 Lei nº 13.460/2017 – Defesa do Usuário dos Serviços Públicos e alterações.",
    "5.4 Estratégia Nacional de Governo Digital - Decreto 11.260/22 e alterações; Decreto nº 10.332/2020.",
    "5.5 Estratégia Brasileira para a Transformação Digital (Decreto 9319/18 e suas alterações)."
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

print("✅ Card criado com checklist estruturado no novo quadro!")

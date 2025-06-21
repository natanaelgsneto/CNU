import requests

# ——————————————————————————
# AUTENTICAÇÃO E CONFIGURAÇÃO
# ——————————————————————————
API_KEY = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = 'CqZynf3b'
LIST_NAME = 'Planejamento'
CARD_NAME = '📘 Eixo Temático 4 – DESENVOLVIMENTO DE SOFTWARE (Checklist Estruturado)'

# ——————————————————————————
# CHECKLIST FORMATADO
# ——————————————————————————
checklist_items = [
    "1 Programação e estruturas de dados.",
    "1.1 Linguagens de programação Python e Java.",
    "1.2 Orientação a objetos: conceitos básicos, padrões de projeto.",
    "1.3 Algoritmos de busca e ordenação.",
    "1.4 Estruturas lineares: lista encadeada, pilha, fila.",
    "1.5 Árvores: formas de representação, recursão em árvores, árvores binárias, árvores binárias de busca, filas de prioridades, árvores balanceadas.",

    "2 Programação Web.",
    "2.1 Conceitos fundamentais de programação para a Web. Linguagens: HTML, XML, CSS, JavaScript.",
    "2.2 Navegadores.",
    "2.3 Frameworks de desenvolvimento para a Web.",
    "2.4 Servidores Web.",

    "3 Desenvolvimento para plataformas móveis.",
    "3.1 Plataformas de programação.",
    "3.2 Emuladores e padrões de programação para smartphones e tablets.",
    "3.3 Principais componentes de interface com o usuário.",
    "3.4 Tecnologias de persistência de dados em dispositivos móveis.",

    "4 Engenharia de software.",
    "4.1 Processos ágeis.",
    "4.2 Engenharia de requisitos.",
    "4.3 Ideação e especificação ágil.",
    "4.4 Arquitetura MVC e princípios de projeto.",
    "4.5 Testes unitários.",
    "4.6 Revisões de software modernas.",
    "4.7 DevOps (controle de versões, integração contínua e deployment contínuo).",
    "4.8 Testes de aceitação.",

    "5 Banco de dados.",
    "5.1 Projeto de banco de dados: projeto conceitual, lógico e físico.",
    "5.2 Abordagem Entidade-Relacionamento (E-R).",
    "5.3 Modelo relacional: conceitos, restrições de integridade, mapeamento de modelos E-R para esquemas relacionais.",
    "5.4 Dependências funcionais e normalização.",
    "5.5 Linguagem SQL: DDL, DML, restrições de integridade, visões, autorização de acesso.",
    "5.6 Sistemas de gerência de bancos de dados.",
    "5.7 Bancos de dados NoSQL: definição, orientação a agregados, tipos de SGBD NoSQL: chave-valor, documentos, colunas, grafos.",

    "6 Arquitetura e tecnologias de sistemas de informação.",
    "6.1 Conceitos básicos.",
    "6.2 Workflow e gerenciamento eletrônico de documentos."
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

print("✅ Card com checklist do Eixo 4 criado com sucesso!")

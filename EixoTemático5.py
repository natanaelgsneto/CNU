import requests

# ——————————————————————————
# AUTENTICAÇÃO E CONFIGURAÇÃO
# ——————————————————————————
API_KEY = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = 'CqZynf3b'
LIST_NAME = 'Planejamento'
CARD_NAME = '📘 Eixo Temático 5 – IA, Apoio à Decisão e Estatística (Checklist Estruturado)'

# ——————————————————————————
# CHECKLIST FORMATADO
# ——————————————————————————
checklist_items = [
    "1 Big Data.",
    "1.1 Definição de Big Data.",
    "1.2 Bancos de dados na nuvem.",
    "1.2.1 O paradigma de computação na nuvem.",
    "1.2.2 Requisitos de gerência de dados na nuvem.",
    "1.2.3 Categorias de bancos de dados na nuvem.",
    "1.3 Infraestruturas para Big Data: Hadoop, Spark, Kafka.",

    "2 Data Warehouse.",
    "2.1 Definição e características de um Data Warehouse.",
    "2.2 Data Mart.",
    "2.3 OLTP e OLAP.",
    "2.4 Modelagem Multidimensional.",
    "2.5 Bancos de Dados Multidimensionais.",
    "2.6 Projeto de Data Warehouse.",
    "2.7 ETL: extração, transformação e carga.",

    "3 Mineração de Dados e Descoberta de Conhecimento.",
    "3.1 Conceitos do processo KDD.",
    "3.2 Metodologia de KDD.",
    "3.3 Métodos de Data Mining.",
    "3.4 Pré-processamento de dados.",
    "3.5 Mineração de dados: classificação, regressão, agrupamento, regras de associação, sumarização, modelagem de dependências, detecção de tendências e exceções.",
    "3.6 Visualização de Dados.",

    "4 Aprendizado de máquina.",
    "4.1 Tipos: supervisionado, não supervisionado, por reforço.",
    "4.2 Algoritmos: regressão, árvores de decisão, redes neurais, SVM, agrupamento.",

    "5 Estatística.",
    "5.1 Medidas de tendência central.",
    "5.2 Medidas separatrizes.",
    "5.3 Medidas de dispersão.",
    "5.4 Assimetria, curtose, correlação de Pearson, contingência de Pearson.",
    "5.5 Gráficos, tabelas e medidas descritivas.",

    "6 Probabilidade.",
    "6.1 Probabilidade condicional e independência.",
    "6.2 Variáveis aleatórias: discretas e contínuas.",

    "7 Inferência Estatística.",
    "7.1 População e amostra.",
    "7.2 Seleção de amostra.",
    "7.3 Estatística e parâmetro.",
    "7.4 Distribuições amostrais.",

    "8 Estimação.",
    "8.1 Estimação pontual.",
    "8.2 Estimação intervalar.",

    "9 Testes de hipóteses.",
    "9.1 Teste sobre a média de uma população.",
    "9.2 Teste com amostras independentes.",
    "9.3 Teste com amostras dependentes (pareadas).",
    "9.4 Testes de homogeneidade.",
    "9.5 Teste de independência.",
    "9.6 Teste para o coeficiente de correlação.",

    "10 Regressão.",
    "10.1 Diagrama de dispersão.",
    "10.2 Reta de regressão e mínimos quadrados.",
    "10.3 Regressão linear simples.",
    "10.4 Intervalos de confiança e de predição.",

    "11 Amostragem.",
    "11.1 Amostragem probabilística: simples, estratificada, sistemática, por conglomerados.",
    "11.2 Amostragem não probabilística.",

    "12 Entidades Discretas e Contínuas; Algoritmos; Operações Lógicas, Aritméticas, Trigonométricas e Estatísticas."
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

print("✅ Card com checklist do Eixo 5 criado com sucesso!")

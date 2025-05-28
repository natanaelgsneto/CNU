import pandas as pd
import requests

# ——————————————————————————
# CONFIGURAÇÃO
# ——————————————————————————
API_KEY  = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN    = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = 'BpZvIIKw'  # o código que você já instalou

CSV_PATH = 'C:\\Users\\Natanael\\PycharmProjects\\pythonProject\\Cronograma_Estudos_CNU_2025_TI.csv'  # certifique-se de estar no mesmo diretório

# Nome exato das listas no seu quadro:
LISTAS = ['Planejamento', 'Execução', 'Revisão']

# ——————————————————————————
# FUNÇÕES AUXILIARES
# ——————————————————————————

def trello_post(endpoint, params):
    url = f"https://api.trello.com/1/{endpoint}"
    params.update({'key': API_KEY, 'token': TOKEN})
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json()

def get_or_create_lists():
    """Retorna um dict {nome_da_lista: id_da_lista}"""
    ids = {}
    for nome in LISTAS:
        # cria a lista no final do board
        data = trello_post(f"boards/{BOARD_ID}/lists", {'name': nome, 'pos': 'bottom'})
        ids[nome] = data['id']
        print(f"✔ Lista criada: {nome}")
    return ids

def get_or_create_labels(label_names):
    """Retorna um dict {nome_da_label: id_da_label}"""
    ids = {}
    for nome in label_names:
        data = trello_post(f"boards/{BOARD_ID}/labels", {'name': nome, 'color': 'null'})
        ids[nome] = data['id']
        print(f"✔ Etiqueta criada: {nome}")
    return ids

def create_card(name, list_id, label_ids):
    params = {'name': name, 'idList': list_id}
    if label_ids:
        params['idLabels'] = ','.join(label_ids)
    trello_post("cards", params)
    print(f"  • Cartão criado: {name}")

# ——————————————————————————
# 1) Carrega o CSV e extrai os dias/blocos
# ——————————————————————————
df = pd.read_csv(CSV_PATH, sep=';', encoding='latin1')

# Extrai todas as labels únicas nos blocos
todas_labels = pd.concat([df['Bloco 1'], df['Bloco 2'], df['Bloco 3']])\
                 .dropna().astype(str).str.strip().unique().tolist()

# ——————————————————————————
# 2) Cria listas e etiquetas no Trello
# ——————————————————————————
list_ids  = get_or_create_lists()
label_ids = get_or_create_labels(todas_labels)

# ——————————————————————————
# 3) Cria um cartão para cada dia e cada bloco
# ——————————————————————————
for idx, row in df.iterrows():
    dia = row['Dia']
    for bloco_num in [1, 2, 3]:
        materia = row[f'Bloco {bloco_num}'].strip()
        # pula se estiver em branco ou for “— descanso —”
        if materia == '' or 'descanso' in materia.lower():
            continue

        # título no formato “Bloco X - Dia: Matéria”
        titulo = f"Bloco {bloco_num} - {dia}: {materia}"
        lst_id = list_ids['Planejamento']  # todas vão para “Planejamento”; ajuste aqui se quiser outra lista
        lbl_id = label_ids.get(materia)

        create_card(titulo, lst_id, [lbl_id] if lbl_id else [])

print("\nTudo pronto! ✔ Seus cartões foram importados no Trello.")

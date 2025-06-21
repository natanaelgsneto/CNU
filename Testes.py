import pandas as pd
import requests

# ——————————————————————————
# CONFIGURAÇÃO
# ——————————————————————————
API_KEY  = '9116e28fafc2e24b1b18ff417fea4dc8'
TOKEN    = 'ATTA83b0dae8e025d5a203f37ffea918c4fd66f7d69d7ed03799d4ce84016f4a09833BB6908E'
BOARD_ID = '4Yps7asb'
CSV_PATH = 'Cronograma_Estudos_CNU_2025_TI.csv'

LISTAS = ['Planejamento', 'Execução', 'Revisão']

# ——————————————————————————
# 1) Defina o vetor de assuntos na ordem exata do edital
# ——————————————————————————
# Você deve transcrever cada item numerado (por exemplo, "1.1 Introdução às políticas públicas: conceitos e tipologias.")
# para esta lista, na ordem em que eles aparecem no edital.
assuntos = [
    # CONHECIMENTOS GERAIS
    "1.1 Introdução às políticas públicas: conceitos e tipologias.",
    "1.2 Ciclos de políticas públicas: agenda e formulação; processos de decisão; implementação; monitoramento e avaliação.",
    "1.3 Institucionalização das políticas em Direitos Humanos como políticas de Estado.",
    "1.4 Federalismo e descentralização de políticas públicas no Brasil.",
    "2.1 Estado de direito e a CF/88: consolidação da democracia, representação política e participação cidadã.",
    "2.2 Divisão e coordenação de Poderes da República. ",
    "2.3 Presidencialismo como sistema de governo: noções gerais, capacidades governativas e especificidades do caso brasileiro",
     "2.4 Efetivação e reparação de Direitos Humanos: memória, autoritarismo e violência de Estado. ",
    "2.5 Programa Nacional de Direitos Humanos PNDH-3 (Decreto nº 7.037/2009).",
    "2.6 Combate às discriminações, desigualdades e injustiças: de renda, regional,racial, etária e de gênero.",
    "2.7 Desenvolvimento sustentável, meio ambiente e mudança climática.",
    "3 ÉTICA e INTEGRIDADE",
    "3.1 Princípios e valores éticos do serviço público, seus direitos e deveres à luz do artigo 37 da Constituição Federal de 1988, e do Código de Ética Profissional do Servidor Público Civil do Poder Executivo Federal (Decreto nº 1.171/1994). ",
    

]

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
    ids = {}
    for nome in LISTAS:
        data = trello_post(f"boards/{BOARD_ID}/lists", {'name': nome, 'pos': 'bottom'})
        ids[nome] = data['id']
    return ids

def create_card(name, list_id, desc=None):
    params = {'name': name, 'idList': list_id}
    if desc:
        params['desc'] = desc
    trello_post("cards", params)
    print(f"✔ Cartão: {name} — {desc}")

# ——————————————————————————
# 2) Carrega CSV
# ——————————————————————————
df = pd.read_csv(CSV_PATH, sep=';', encoding='latin1')

list_ids = get_or_create_lists()

# contador global de assuntos
contador = 0

# ——————————————————————————
# 3) Cria cartões e injeta o assunto correspondente
# ——————————————————————————
for idx, row in df.iterrows():
    dia = row['Dia']
    for bloco_num in [1, 2, 3]:
        materia = str(row.get(f'Bloco {bloco_num}', '')).strip()
        if not materia or 'descanso' in materia.lower():
            continue

        # título padrão
        titulo = f"Bloco {bloco_num} - {dia}: {materia}"

        # pega o assunto sequencial; se acabar, para
        if contador < len(assuntos):
            descricao = f"Assunto: {assuntos[contador]}"
        else:
            descricao = ""
        contador += 1

        create_card(titulo, list_ids['Planejamento'], desc=descricao)

print("Todos os cartões com assuntos foram criados!")

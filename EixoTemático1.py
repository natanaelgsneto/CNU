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
# ASSUNTOS – EIXO TEMÁTICO 1 – GESTÃO GOVERNAMENTAL E GOVERNANÇA PÚBLICA
# ——————————————————————————
assuntos = [
    "1 Planejamento e gestão estratégica: conceitos, princípios, etapas, níveis, métodos e ferramentas.",
    "1.1 Balanced Scorecard (BSC).",
    "1.2 Matriz SWOT.",
    "1.3 Estabelecimento de objetivos e metas organizacionais.",
    "1.4 Métodos de desdobramento de objetivos e metas e elaboração de planos de ação e mapas estratégicos.",
    "1.5 Implementação de estratégias.",
    "1.6 Análise de cenários.",
    "1.7 Ferramentas de gestão.",
    "1.8 Metodologias para medição de desempenho.",
    "1.9 Indicadores de desempenho: conceito, formulação e análise.",
    "1.10 Detalhamento da ferramenta de avaliação de desempenho: OKR.",
    "2 Gestão de projetos.",
    "2.1 Conceitos básicos.",
    "2.2 Processos do PMBOK.",
    "2.3 Gerenciamento da integração, do escopo, do tempo, de custos, da qualidade, de recursos humanos, de comunicações, de riscos, de aquisições, de partes interessadas.",
    "2.4 Metodologias ágeis.",
    "3 Gestão de processos de negócio.",
    "3.1 Conceitos da abordagem por processos.",
    "3.2 Técnicas de mapeamento, análise, melhoria e integração de processos.",
    "3.3 Modelagem de processos com BPMN (versão 2.0).",
    "3.4 Desenho de serviços públicos.",
    "4 Gestão de riscos: princípios, objetos, técnicas, modelos nacionais e internacionais, integração ao planejamento.",
    "4.1 Processo de Gestão de Riscos: comunicação, consulta, contextualização, identificação, análise, tratamento, monitoramento e retroalimentação.",
    "4.2 Boas práticas de gestão de Riscos.",
    "5 Inovação na gestão pública.",
    "6 Governo eletrônico; transparência da administração pública; controle social e cidadania; accountability.",
    "7 Comunicação na gestão pública.",
    "8 Compras governamentais.",
    "8.1 Processos de compras e gestão de contratos.",
    "8.2 Contratações de tecnologia da informação.",
    "8.3 Sustentabilidade das contratações.",
    "8.4 Compras centralizadas.",
    "9 Organização sistêmica da administração pública federal.",
    "9.1 Sistemas estruturantes e estruturadores da administração pública federal."
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

        # título do card
        titulo = f"Bloco {bloco_num} - {dia}: {materia}"

        # descrição do card (assunto do edital)
        if contador < len(assuntos):
            descricao = f"Assunto: {assuntos[contador]}"
            contador += 1
        else:
            descricao = "Assunto: (não definido)"

        create_card(titulo, list_ids['Planejamento'], desc=descricao)

print("✅ Todos os cartões do Eixo Temático 1 foram criados!")

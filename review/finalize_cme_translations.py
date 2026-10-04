"""Record the final translation wording checks and shared penile-module UI."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / 'translations'
read = lambda name: json.loads((folder / name).read_text(encoding='utf-8'))
def write(name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

html = (ROOT / 'templates/cme/cme-peniskarzinom.html.in').read_text(encoding='utf-8')
ui = {key: value for key, value in read('cme-salvage-operationen.ui.json').items() if key in html}
ui.update({
    'Peniskarzinom: CME-Modul Facharztniveau': {'en':'Penile cancer: specialist-level CME module','es':'Cáncer de pene: módulo CME de nivel de especialista'},
    'Peniskarzinom: Organerhalt, Lymphknoten und Systemtherapie': {'en':'Penile cancer: organ preservation, lymph nodes and systemic therapy','es':'Cáncer de pene: preservación del órgano, ganglios linfáticos y tratamiento sistémico'},
    'Primärtumor: stadiengerechtes Vorgehen': {'en':'Primary tumour: stage-appropriate management','es':'Tumor primario: tratamiento según el estadio'},
    'Stadium wählen. Angezeigt werden Verfahren, Entscheidung am Rand und Datenbasis. Quellen: Spreda & Protzel 2025, EAU/ASCO 2026.': {'en':'Select a stage. The procedures, margin-related decision and evidence base are shown. Sources: Spreda & Protzel 2025, EAU/ASCO 2026.','es':'Selecciona un estadio. Se muestran los procedimientos, la decisión sobre los márgenes y la base de evidencia. Fuentes: Spreda y Protzel 2025, EAU/ASCO 2026.'},
    'cN0: operatives Staging oder Überwachung?': {'en':'cN0: surgical staging or surveillance?','es':'cN0: ¿estadificación quirúrgica o vigilancia?'},
    'Zutreffende Kriterien ankreuzen. Quellen: Dräger et al. 2025, EAU/ASCO 2026, Abschnitt 5.2.2.': {'en':'Select the applicable criteria. Sources: Dräger et al. 2025, EAU/ASCO 2026, section 5.2.2.','es':'Marca los criterios que se cumplen. Fuentes: Dräger et al. 2025, EAU/ASCO 2026, apartado 5.2.2.'},
    'Verfahren': {'en':'Procedure','es':'Procedimiento'},
    'Entscheidung': {'en':'Decision','es':'Decisión'},
    'Datenbasis': {'en':'Evidence base','es':'Base de evidencia'}
})
write('cme-peniskarzinom.ui.json', ui)
data = read('cme-peniskarzinom.en.json')
q = next(q for q in data['questions'] if q['n'] == 7)
q['merk'] = q['merk'].replace('then surgery for a response', 'then surgery if there is a response')
write('cme-peniskarzinom.en.json', data)
data = read('cme-salvage-operationen.es.json')
data['hcg'][0]['data'] = data['hcg'][0]['data'].replace('recuperación durante más de ocho meses', 'recuperación a lo largo de ocho meses')
write('cme-salvage-operationen.es.json', data)
data = read('cme-hodentumor-heft-teil3.es.json')
q = next(q for q in data['questions'] if q['n'] == 14)
q['flag'] = q['flag'].replace('65 o 71 %', '65 a 71 %')
write('cme-hodentumor-heft-teil3.es.json', data)
data = read('cme-seminom-IIAB.es.json')
def node_term(value):
    if isinstance(value, dict):
        return {key: node_term(child) for key, child in value.items()}
    if isinstance(value, list):
        return [node_term(child) for child in value]
    if isinstance(value, str):
        return value.replace('radioterapia de campo afectado', 'radioterapia dirigida a los ganglios afectados').replace('Radioterapia de campo afectado', 'Radioterapia dirigida a los ganglios afectados')
    return value
data = node_term(data)
q = next(q for q in data['questions'] if q['n'] == 9)
q['opts']['A'] = 'Radioterapia dirigida a los ganglios afectados y después un ciclo de carboplatino AUC 7'
q['opts']['D'] = 'Un ciclo de etopósido y cisplatino, después radioterapia dirigida a los ganglios afectados con 30 Gy'
write('cme-seminom-IIAB.es.json', data)
print('Shared UI completed; conditional surgery wording and eight-month recovery wording checked.')

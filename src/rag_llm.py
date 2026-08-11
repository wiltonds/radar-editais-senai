import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- carrega o indice ja salvo pelo catalogo_rag.py ---
emb = np.load("emb_catalogo.npy")
cat = pd.read_json("catalogo_indexado.json")
cursos = cat["Curso"].tolist()
print(f"Indice carregado: {len(cursos)} servicos")

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODELO = "qwen2.5-7b-instruct-1m"


def pesca_candidatos(texto, n=5):
    """EMBEDDING: acha os n servicos mais proximos entre os 986 (rapido, matematico)."""
    q = model.encode([texto], normalize_embeddings=True)
    sims = (emb @ q.T).ravel()
    top = np.argsort(-sims)[:n]
    return [(cursos[i], float(sims[i])) for i in top]


def decide(objeto, candidatos):
    """LLM: le os candidatos pescados e escolhe o melhor, ou diz que nenhum serve."""
    lista = "\n".join(f"- {nome}" for nome, _ in candidatos)
    sistema = """Voce liga um edital a um curso/servico do SENAI/SESI.
Recebe o objeto do edital e uma lista curta de servicos candidatos.
Escolha o UNICO mais aderente da lista. Se NENHUM fizer sentido real, responda "nenhum".
Responda so o nome do servico escolhido (ou "nenhum"), nada mais."""
    resp = client.chat.completions.create(
        model=MODELO, temperature=0,
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": f"EDITAL: {objeto}\n\nCANDIDATOS:\n{lista}"},
        ],
    )
    return resp.choices[0].message.content.strip()


editais = [
    "Implantacao de sistema de energia solar fotovoltaica",
    "Instalacao e manutencao de aparelhos de ar condicionado",
    "Servicos de capa asfaltica em concreto betuminoso para vias urbanas",
    "Contratacao de servicos terceirizados com muitos funcionarios",
    "Manutencao industrial predial preventiva e corretiva",
]

for ed in editais:
    cands = pesca_candidatos(ed)
    escolha = decide(ed, cands)
    print(f"\nEDITAL: {ed}")
    print("  candidatos do embedding:")
    for nome, s in cands:
        print(f"     {s:.2f}  {nome}")
    print(f"  >>> LLM escolheu: {escolha}")
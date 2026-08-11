import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from catalogo_fichas import FICHAS, ficha_texto

print(f"{len(FICHAS)} fichas ricas carregadas")

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
textos = [ficha_texto(f) for f in FICHAS]
emb = model.encode(textos, normalize_embeddings=True, show_progress_bar=True)
np.save("emb_fichas.npy", emb)
print("Indice das fichas salvo\n")

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODELO = "qwen2.5-7b-instruct-1m"
CORTE = 0.30


def pesca(texto_edital, n=5):
    q = model.encode([texto_edital], normalize_embeddings=True)
    sims = (emb @ q.T).ravel()
    top = np.argsort(-sims)[:n]
    return [(FICHAS[i], float(sims[i])) for i in top]


def decide(objeto, candidatos):
    lista = "\n".join(f"- {f['servico']}" for f, _ in candidatos)
    sistema = """Voce liga um edital a um servico do SENAI/SESI.
Escolha da lista o UNICO servico mais aderente ao edital. Se nenhum servir de verdade, responda "nenhum".
Responda so o nome exato do servico escolhido (ou "nenhum")."""
    resp = client.chat.completions.create(
        model=MODELO, temperature=0,
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": f"EDITAL: {objeto}\n\nSERVICOS:\n{lista}"},
        ],
    )
    return resp.choices[0].message.content.strip()


editais = [
    "Implantacao de sistema de energia solar fotovoltaica com instalacao em telhado",
    "Instalacao e manutencao de aparelhos de ar condicionado split",
    "Servicos de capa asfaltica em concreto betuminoso para vias urbanas",
    "Contratacao de servicos terceirizados com muitos funcionarios",
    "Manutencao industrial predial preventiva e corretiva",
    "Limpeza e manutencao de tanques e reservatorios de agua",
    "Aquisicao de medicamentos para a rede municipal de saude",
]

for ed in editais:
    cands = pesca(ed)
    escolha = decide(ed, cands)
    atuacao = ""
    for f, _ in cands:
        if f["servico"].lower() in escolha.lower() or escolha.lower() in f["servico"].lower():
            atuacao = f["atuacao"]
    print(f"\nEDITAL: {ed}")
    for f, s in cands:
        marca = "" if s >= CORTE else "  (fraco)"
        print(f"   {s:.2f}  [{f['atuacao']:9}] {f['servico']}{marca}")
    print(f"  >>> LLM escolheu: {escolha}  [{atuacao}]")
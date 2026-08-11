import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from catalogo_fichas import FICHAS, ficha_texto

_model = None
_emb = None
_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODELO = "qwen2.5-7b-instruct-1m"
PISO_EMBEDDING = 0.32   # se o melhor candidato ficar abaixo disso, ai sim "nenhum"


def _carrega():
    global _model, _emb
    if _model is None:
        print("  (carregando modelo de embeddings e indexando fichas...)")
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        textos = [ficha_texto(f) for f in FICHAS]
        _emb = _model.encode(textos, normalize_embeddings=True)


def busca_servico(objeto_edital, categoria, n=5):
    _carrega()
    q = _model.encode([objeto_edital], normalize_embeddings=True)
    sims = (_emb @ q.T).ravel()
    top = np.argsort(-sims)[:n]
    candidatos = [FICHAS[i] for i in top]
    melhor_sim = float(sims[top[0]])

    # Se nem o embedding achou nada minimamente proximo, ai sim descarta.
    if melhor_sim < PISO_EMBEDDING:
        return "nenhum", "", ""

    lista = "\n".join(f"{idx+1}. {f['servico']}: {f['texto']}"
                      for idx, f in enumerate(candidatos))

    if categoria == "mao_de_obra":
        contexto = """A empresa que VENCER este edital vai executar a obra/servico com trabalhadores
que precisam de qualificacao e Normas Regulamentadoras (NR). Escolha o servico que a EQUIPE
da empresa vencedora vai precisar. Ex: energia solar -> NR-10/NR-35; ar condicionado -> refrigeracao; obra/asfalto -> NR-18."""
    else:
        contexto = """O orgao contratou algo que o SENAI/SESI pode prestar diretamente.
Escolha o servico mais aderente ao objeto do edital."""

    sistema = f"""{contexto}
Um desses servicos SEMPRE e o mais adequado. Escolha o MELHOR pelo NUMERO (1 a {len(candidatos)}).
Responda APENAS o numero, nada mais."""

    resp = _client.chat.completions.create(
        model=MODELO, temperature=0,
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": f"EDITAL: {objeto_edital}\n\nSERVICOS:\n{lista}"},
        ],
    )
    escolha = resp.choices[0].message.content.strip()

    # pega o numero que o LLM respondeu; se falhar, usa o 1o (mais proximo do embedding)
    idx = 0
    for ch in escolha:
        if ch.isdigit():
            n_esc = int(ch) - 1
            if 0 <= n_esc < len(candidatos):
                idx = n_esc
            break

    f = candidatos[idx]
    return f["servico"], f["atuacao"], f["texto"][:90]
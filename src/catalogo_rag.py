import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

CAMINHO = r"C:\Users\wilton.costa\Downloads\ver_catalogo.xlsx"

# Gatilhos: linguagem de EDITAL -> reforca certos servicos.
# Nao precisa cobrir tudo. So os casos que mais aparecem em licitacao.
def texto_ficha(categoria, nome):
    cat = str(categoria).strip()
    if len(cat) > 40:            # categorias gigantes = SST
        cat = "seguranca e saude do trabalho"
    return f"{cat}: {nome}"

# 1. Carrega e monta as fichas
df = pd.read_excel(CAMINHO, sheet_name="Catalogo")
df = df.dropna(subset=["Curso"]).copy()
df["Curso"] = df["Curso"].str.strip()
df = df.drop_duplicates(subset=["Curso"]).reset_index(drop=True)
df["ficha"] = df.apply(lambda r: texto_ficha(r["categoria"], r["Curso"]), axis=1)
print(f"{len(df)} servicos com ficha montada")

# 2. Gera os embeddings das FICHAS (nao mais so do nome)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
emb = model.encode(df["ficha"].tolist(), normalize_embeddings=True, show_progress_bar=True)

# 3. Salva indice pra reusar sem recalcular
np.save("emb_catalogo.npy", emb)
df[["categoria", "Curso", "ficha"]].to_json("catalogo_indexado.json",
                                             orient="records", force_ascii=False)
print("Indice salvo: emb_catalogo.npy + catalogo_indexado.json\n")

# 4. TESTE: compara os editais problematicos, agora com ficha rica + corte
CORTE = 0.45   # abaixo disso = match fraco, nao forca
editais = [
    "Implantacao de sistema de energia solar fotovoltaica",
    "Instalacao e manutencao de aparelhos de ar condicionado",
    "Servicos de capa asfaltica em concreto betuminoso para vias urbanas",
    "Contratacao de servicos terceirizados com muitos funcionarios",
]
cursos = df["Curso"].tolist()
for ed in editais:
    q = model.encode([ed], normalize_embeddings=True)
    sims = (emb @ q.T).ravel()
    top = np.argsort(-sims)[:5]
    print(f"EDITAL: {ed}")
    for i in top:
        marca = "" if sims[i] >= CORTE else "  (abaixo do corte)"
        print(f"   {sims[i]:.2f}  {cursos[i]}{marca}")
    print()
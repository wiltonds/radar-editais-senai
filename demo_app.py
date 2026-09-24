"""Recruiter-facing demo of the public-procurement radar.
Synthetic examples only; no production tender/customer data.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Radar de Editais | Demo", page_icon="📡", layout="wide")
st.title("📡 Radar de Editais — Commercial Intelligence")
st.caption("Demo executável · dados sintéticos · PNCP → classificação → matching → priorização")

editais=pd.DataFrame([
{"Objeto":"Contratação de treinamento em segurança de máquinas NR-12","Órgão":"Prefeitura Municipal de Maceió","Município":"Maceió/AL","Categoria":"CONCORRER","Fit":94,"Oferta":"Treinamento NR-12"},
{"Objeto":"Serviços de manutenção preventiva de equipamentos industriais","Órgão":"Instituto Federal","Município":"Maceió/AL","Categoria":"CONCORRER","Fit":88,"Oferta":"Manutenção Industrial"},
{"Objeto":"Aquisição de capacitação para produtividade e processos","Órgão":"Município de Rio Largo","Município":"Rio Largo/AL","Categoria":"MONITORAR","Fit":76,"Oferta":"Gestão e Produtividade"},
])
c1,c2,c3,c4=st.columns(4)
for c,t,v,s in [(c1,"Editais triados","128","rodada demonstrativa"),(c2,"Alta aderência","17","fit ≥ 80"),(c3,"Para concorrer","8","serviço aderente"),(c4,"Prospectáveis","11","vencedor / mercado")]:
    with c: st.metric(t,v,s)
st.divider()
f=st.selectbox("Filtrar por estratégia",["Todos","CONCORRER","MONITORAR"])
view=editais if f=="Todos" else editais[editais.Categoria==f]
st.subheader("Oportunidades priorizadas")
for _,e in view.iterrows():
    with st.container(border=True):
        a,b,c=st.columns([6,2,2])
        a.markdown(f"**{e.Objeto}**")
        a.caption(f"{e.Órgão} · {e.Município}")
        b.metric("Fit",f"{e.Fit}%")
        c.success(e.Categoria)
        st.write(f"**Oferta relacionada:** {e.Oferta}")
        st.caption("Evidence → retrieval → AI reasoning → validation → commercial action")
st.info("DEMO — objetos, órgãos, scores e ofertas são sintéticos e servem apenas para demonstrar o fluxo.")

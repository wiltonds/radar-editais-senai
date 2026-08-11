# radar_completo.py — roda os dois fluxos e gera UM briefing unificado.
from datetime import datetime
import webbrowser, os

print("=== RADAR COMERCIAL COMPLETO ===\n")

# --- 1. EDITAIS ABERTOS (roda o grafo que voce ja tem) ---
print("[1/2] Rodando radar de editais...")
from grafo import app
resultado = app.invoke({"editais": [], "triados": [], "cards": []})
cards_editais = resultado.get("cards", [])
concorrer = [e for e in cards_editais if e.get("categoria") == "servico"]
prosp_edital = [e for e in cards_editais if e.get("categoria") == "mao_de_obra"]

# --- 2. VENCEDORES (roda o coletor de vencedores) ---
print("\n[2/2] Coletando vencedores recentes...")
from vencedores import coleta_leads
quentes, de_fora = coleta_leads()

# --- 3. MONTA O BRIEFING UNIFICADO ---
def card_edital(e):
    return f"""<div class="card"><div class="corpo">
      <div class="obj">{e.get('objeto','')[:120]}</div>
      <div class="meta">{e.get('orgao','')} — {e.get('municipio','')}/AL</div>
      <div class="linha"><b>Oferta:</b> {e.get('servico_match','-')}</div>
      </div></div>"""

def card_venc(v):
    c = v["contato"]
    if c:
        acao = f"<div class='acao'><b>Contato:</b> {c['telefone']} · {c['email']} · {c['ramo']} · {c['municipio']}</div>"
        tag = "<span class='tag q'>LEAD QUENTE · AL</span>"
    else:
        acao = "<div class='acao aviso'><b>Empresa de fora</b> — buscar contato (site/edital)</div>"
        tag = "<span class='tag f'>BUSCAR CONTATO</span>"
    return f"""<div class="card"><div class="corpo">{tag}
      <div class="obj">{v['nome']}</div>
      <div class="meta">Ganhou: {v['objeto'][:90]}</div>
      {acao}</div></div>"""

def secao(titulo, sub, cards, render):
    corpo = "".join(render(x) for x in cards) if cards else "<p class='vazio'>Nenhum nesta rodada.</p>"
    return f"<h2>{titulo}</h2><div class='sub'>{sub}</div>{corpo}"

html = f"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<title>Radar Comercial — SENAI/SESI Alagoas</title><style>
body{{font-family:system-ui,Arial,sans-serif;background:#f1f5f9;margin:0;padding:24px;color:#0f172a}}
h1{{font-size:22px;margin:0 0 2px}} .data{{color:#64748b;font-size:13px;margin-bottom:16px}}
h2{{font-size:16px;margin:26px 0 2px;padding-bottom:4px;border-bottom:2px solid #e2e8f0}}
.sub{{color:#64748b;font-size:12px;margin:2px 0 12px}}
.card{{background:#fff;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:10px}}
.corpo{{padding:12px 16px}} .obj{{font-weight:600;margin-bottom:3px}}
.meta{{color:#475569;font-size:13px;margin-bottom:6px}} .linha{{font-size:13px;margin:2px 0}}
.acao{{font-size:13px;margin-top:8px;padding:6px 10px;background:#eff6ff;border-left:3px solid #3b82f6;border-radius:4px}}
.acao.aviso{{background:#fef3c7;border-left-color:#d97706}}
.tag{{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;margin-bottom:6px}}
.tag.q{{background:#dcfce7;color:#166534}} .tag.f{{background:#fef3c7;color:#92400e}}
.vazio{{color:#94a3b8;font-style:italic}}
</style></head><body>
<h1>Radar Comercial — SENAI/SESI Alagoas</h1>
<div class="data">Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
{secao("1. Oportunidades para CONCORRER", "Editais abertos onde o SENAI/SESI presta. Para a licitacao.", concorrer, card_edital)}
{secao("2. Editais para acompanhar", "Edital aberto que nao e nosso, mas quem vencer sera cliente.", prosp_edital, card_edital)}
{secao("3. Empresas que JA venceram (prospectar agora)", "Contratos homologados. Lead pronto para a Ana.", quentes + de_fora, card_venc)}
</body></html>"""

caminho = os.path.abspath("briefing_completo.html")
with open(caminho, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n>>> Briefing completo gerado: {caminho}")
print(f"    Concorrer: {len(concorrer)} | Acompanhar: {len(prosp_edital)} | Vencedores: {len(quentes)+len(de_fora)}")
webbrowser.open(caminho)
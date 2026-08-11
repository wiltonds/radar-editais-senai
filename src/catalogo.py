# CATÁLOGO SEMENTE de serviços SENAI/SESI Alagoas.
# Ponto de partida enxuto pro MVP — depois você troca pelo catálogo real.
CATALOGO = [
    {"unidade": "SENAI", "servico": "Cursos de qualificação profissional (eletricista, refrigeração, mecânica, solda)", "para": "trabalhadores que precisam de habilitação técnica"},
    {"unidade": "SENAI", "servico": "Treinamentos de Normas Regulamentadoras (NR-10, NR-35, NR-12, NR-33)", "para": "empresas com trabalho em altura, elétrica, máquinas ou espaço confinado"},
    {"unidade": "SENAI", "servico": "Consultoria em produtividade e Lean Manufacturing", "para": "indústrias querendo reduzir custo e desperdício"},
    {"unidade": "SENAI", "servico": "Consultoria em eficiência energética", "para": "empresas com alto consumo de energia"},
    {"unidade": "SENAI", "servico": "Metrologia e calibração de instrumentos", "para": "indústrias com equipamentos de medição"},
    {"unidade": "SENAI", "servico": "Ensaios laboratoriais de materiais e produtos", "para": "indústrias que precisam certificar qualidade"},
    {"unidade": "SENAI", "servico": "Consultoria em inovação e transformação digital industrial", "para": "indústrias modernizando processos"},
    {"unidade": "SESI", "servico": "Elaboração de PGR e PCMSO (segurança e saúde ocupacional)", "para": "toda empresa com funcionários CLT"},
    {"unidade": "SESI", "servico": "Exames ocupacionais e ASO", "para": "empresas admitindo ou mantendo trabalhadores"},
    {"unidade": "SESI", "servico": "Laudos técnicos (LTCAT, insalubridade, periculosidade)", "para": "empresas com riscos ambientais"},
    {"unidade": "SESI", "servico": "Treinamento de CIPA e brigada de incêndio", "para": "empresas que precisam cumprir NR-5 e NR-23"},
    {"unidade": "SESI", "servico": "Ginástica laboral e promoção da saúde", "para": "empresas com muitos funcionários"},
]

def catalogo_texto():
    """Devolve o catálogo como texto compacto pra caber no prompt."""
    linhas = [f'{i}. [{s["unidade"]}] {s["servico"]} (para: {s["para"]})'
              for i, s in enumerate(CATALOGO, 1)]
    return "\n".join(linhas)
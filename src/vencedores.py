# vencedores.py — puxa contratos homologados no PNCP, filtra por palavra-chave,
# cruza com a base do DW e marca lead QUENTE (AL, com contato) vs DE FORA (sem contato).
import requests
import time
import unicodedata
from datetime import date, timedelta
from cruzamento import busca_contato

BASE = "https://pncp.gov.br/api/consulta/v1/contratos"

LIXO = ["alienacao", "mercadoria apreendida", "agua mineral", "gas liquefeito",
        "genero alimenticio", "silhueta", "cesta basica", "medicamento",
        "combustivel", "locacao de veiculo"]

OPORTUNIDADE = ["obra", "construcao", "pavimenta", "asfalt", "eletric", "instalacao",
                "reforma", "manutencao", "edificacao", "engenharia", "climatiza",
                "ar condicionado", "refrigera", "consultoria", "capacita",
                "treinamento", "mao de obra", "servico especializ"]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")


def triagem(objeto):
    o = sem_acento(objeto)
    if any(sem_acento(l) in o for l in LIXO):
        return "descarta"
    if any(sem_acento(p) in o for p in OPORTUNIDADE):
        return "oportunidade"
    return "revisar"


def puxa_contratos(uf="AL", dias_atras=90, paginas=4):
    """Puxa varias paginas de contratos (mais amostra = mais empresas locais)."""
    data_fim = date.today()
    data_ini = data_fim - timedelta(days=dias_atras)
    todos = []
    for pg in range(1, paginas + 1):
        params = {
            "dataInicial": data_ini.strftime("%Y%m%d"),
            "dataFinal": data_fim.strftime("%Y%m%d"),
            "uf": uf, "pagina": pg, "tamanhoPagina": 50,
        }
        for tentativa in range(1, 4):
            try:
                r = requests.get(BASE, params=params, headers={"accept": "*/*"}, timeout=60)
                r.raise_for_status()
                dados = r.json().get("data") or []
                todos.extend(dados)
                if not dados:
                    return todos   # acabaram as paginas
                break
            except requests.exceptions.RequestException as e:
                status = getattr(getattr(e, "response", None), "status_code", "?")
                print(f"  (pagina {pg}, tentativa {tentativa} - HTTP {status})")
                time.sleep(5)
    return todos


def main():
    print("Buscando contratos com vencedor em Alagoas (ultimos 90 dias)...\n")
    contratos = puxa_contratos()
    print(f"{len(contratos)} contratos brutos.\n")

    quentes, de_fora = [], []
    for c in contratos:
        objeto = c.get("objetoContrato") or ""
        if triagem(objeto) != "oportunidade":
            continue
        cnpj = c.get("niFornecedor")
        nome_pncp = c.get("nomeRazaoSocialFornecedor")
        if not cnpj:
            continue
        contato = busca_contato(cnpj)
        item = {"nome": nome_pncp, "cnpj": cnpj, "objeto": objeto, "contato": contato}
        (quentes if contato else de_fora).append(item)

    print("=" * 60)
    print(f"LEADS QUENTES (de Alagoas, com contato): {len(quentes)}")
    print("=" * 60)
    for x in quentes:
        c = x["contato"]
        print(f"\n{x['nome']}  (CNPJ {x['cnpj']})")
        print(f"  Ganhou: {x['objeto'][:65]}")
        print(f"  >> tel {c['telefone']} | {c['email']} | {c['ramo']} | {c['municipio']}")

    print("\n" + "=" * 60)
    print(f"LEADS DE FORA (buscar contato): {len(de_fora)}")
    print("=" * 60)
    for x in de_fora:
        print(f"\n{x['nome']}  (CNPJ {x['cnpj']})")
        print(f"  Ganhou: {x['objeto'][:65]}")
        print(f"  >> nao esta na base de AL - Ana busca contato (site/edital)")

def coleta_leads():
    """Versao que DEVOLVE os leads (em vez de so imprimir) - usada pelo radar_completo."""
    contratos = puxa_contratos()
    quentes, de_fora = [], []
    for c in contratos:
        objeto = c.get("objetoContrato") or ""
        if triagem(objeto) != "oportunidade":
            continue
        cnpj = c.get("niFornecedor")
        nome = c.get("nomeRazaoSocialFornecedor")
        if not cnpj:
            continue
        contato = busca_contato(cnpj)
        item = {"nome": nome, "cnpj": cnpj, "objeto": objeto, "contato": contato}
        (quentes if contato else de_fora).append(item)
    return quentes, de_fora
if __name__ == "__main__":
    main()
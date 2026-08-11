# Radar de Editais — Inteligência Comercial com IA Local

Agente de IA que transforma licitações públicas (PNCP) em oportunidades comerciais
priorizadas, rodando **100% local** (sem nuvem, sem custo por uso, sem expor dados).

Desenvolvido como prova de conceito de inteligência comercial aplicada à indústria.

## O que faz

Monitora editais e contratos públicos de Alagoas e gera um briefing com três frentes:

1. **Concorrer** — editais que a instituição pode atender diretamente.
2. **Acompanhar** — editais abertos cujo vencedor será cliente potencial.
3. **Prospectar** — empresas que já venceram licitações (lead pronto).

## Arquitetura

- **Coleta:** API pública do PNCP (editais abertos + contratos homologados).
- **Triagem:** classificação em categorias via LLM local + regras de palavra-chave.
- **Match semântico (RAG):** embeddings (sentence-transformers) buscam candidatos
  no catálogo de serviços; um LLM local (via LM Studio) decide o mais aderente.
- **Enriquecimento:** cruzamento de CNPJ do vencedor com base de contatos.
- **Saída:** briefing HTML com score de prioridade.

## Stack

Python · LangGraph · LM Studio (modelo local) · sentence-transformers · pandas

## Como rodar

```bash
pip install -r requirements.txt
# subir um modelo local no LM Studio (endpoint OpenAI-compativel em localhost:1234)
python src/radar_completo.py
```

## Nota sobre dados

Este repositório contém apenas o código. Bases de dados (editais, cadastros de
empresas) não são versionadas por conterem informação sensível.

---
*Projeto autoral — inteligência de mercado aplicada à indústria.*

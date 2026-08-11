from rag import busca_servico

objeto = "Contratacao de empresa especializada em implantacao de sistema de energia solar fotovoltaica"
servico, atuacao, porque = busca_servico(objeto, "mao_de_obra")
print("\n=== RESULTADO ===")
print("servico:", repr(servico))
print("atuacao:", repr(atuacao))


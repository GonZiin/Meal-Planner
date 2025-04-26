from funcoes import * #Usamos o '*' para importar todas funcoes

def main():
    pesquisa, dieta, ingredientes, restricao_dieta = escolherDieta()
    # receitaComIngredientes(ingredientes, 1)
    procurarReceita(pesquisa, dieta, ingredientes, restricao_dieta, 1)

main()
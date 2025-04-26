import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Variáveis globais
# Spoonacular API
url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api = os.getenv("RAPIDAPI_KEY")  # Carregar a chave da API do .env
headers = {
    "x-rapidapi-key": api,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def escolherDieta():
    ingredientes = []
    restricao_dieta = []

    pesquisa = input("Receita que queres procurar? ")
    dieta = input("Que tipo de dieta pretendes seguir? ")

    escolha_ingredientes = input("Desejas usar algum ingrediente especifio (sim/nao)? ").lower()  # Lower para nao ter problema de capitalização
    while escolha_ingredientes == "sim":
        ingredientes.append(input("Que ingrediente pretendes utilizar: ").lower())  # Damos lower para não ter problemas na query da API
        escolha_ingredientes = input("Desejas usar algum outro ingrediente (sim/nao)? ").lower()

    escolha_restricao = input("Tens alguma restrição dietética (sim/nao)? ")
    while escolha_restricao == "sim":
        restricao_dieta.append(input("Que restrição dietética tens? ").lower())
        escolha_restricao = input("Desejas adicionar alguma outra restrição (sim/nao)? ").lower()

    return pesquisa, dieta, ingredientes, restricao_dieta

def receitaPassoAPasso(id):
    url = f"{url_base}/recipes/{id}/analyzedInstructions"
    resposta = requests.get(url, headers=headers)
    instrucoes = resposta.json()  # Retorna lista

    if instrucoes:
        for passo in instrucoes[0]['steps']:  # Primeiro dicionário da lista e queremos ver a chave steps
            print(f"Passo {passo['number']}: {passo['step']}")
    else:
        print("Não foram encontradas instruções para esta receita.")

def receitaComIngredientes(ingredientes, numero):
    ingredientes_formatado = ",".join(ingredientes)  # join faz com que os elementos de uma lista sejam concatenados com a string que escolhemos
    url = f"{url_base}/recipes/findByIngredients"
    # TEM DE SER DICT!
    query = {"ingredients": ingredientes_formatado, "number": str(numero)}
    resposta = requests.get(url, headers=headers, params=query)
    receitas = resposta.json()
    for receita in receitas:
        print(f"Receita: {receita['title']}")
        print(f"Id: {receita['id']}")
        escolha = input("Desejas ver o passo a passo desta receita (sim/nao)? ").lower()
        if escolha == 'sim':
            receitaPassoAPasso(receita['id'])

def procurarReceita(pesquisa, dieta, ingredientes, restricoes, numero):
    ingredientes_formatado = ",".join(ingredientes)
    restricoes_formatado = ",".join(restricoes)

    url = f"{url_base}/recipes/complexSearch"
    query = {"query": pesquisa, "diet": dieta, "intolerances": restricoes_formatado, "includeIngredients": ingredientes_formatado, "number": numero}

    resposta = requests.get(url, headers=headers, params=query)
    # Neste caso como retorna um dicionário, as receitas são o valor da key "results"
    receitas = resposta.json()["results"]
    for receita in receitas:
        print(f"Receita: {receita['title']}")
        print(f"Id: {receita['id']}")
        escolha = input("Desejas ver o passo a passo desta receita (sim/nao)? ").lower()
        if escolha == 'sim':
            receitaPassoAPasso(receita['id'])

def main():
    pesquisa, dieta, ingredientes, restricao_dieta = escolherDieta()
    # receitaComIngredientes(ingredientes, 1)
    procurarReceita(pesquisa, dieta, ingredientes, restricao_dieta, 1)

main()

import requests
import os

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

headers = {
    "x-rapidapi-key": "2ed4484312mshe3540b669887063p1f94ddjsnb3635e32bdbe",
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def escolherDieta():
    ingredientes = []
    restricao_dieta = []
    
    dieta = input("Que tipo de dieta pretendes seguir: ").lower() # damos lower parar nao termos problemas de capitalizacao
    
    escolha = input("Desejas usar ingredientes que já tens no frígorifico? (sim | não): ").lower()
    while escolha == 'sim':
        ingrediente = input("Que ingrediente desejas adicionar: ")
        ingredientes.append(ingrediente)
        escolha = input("Desejas adicionar outro ingrediente? (sim | não): ").lower()
    
    escolha = input("Tens alguma restrição dietética: (sim | não) ").lower()
    while escolha == "sim":
        restricao = input("Introduz a tua restrição dietética: ")
        restricao_dieta.append(restricao)
        escolha = input("Tens alguma outra restrição que desejes adcionar: (sim | não): ").lower()
    
    return dieta, ingredientes, restricao_dieta

def informacaoReceita(id):
    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
    headers = {
        "x-rapidapi-key": "2ed4484312mshe3540b669887063p1f94ddjsnb3635e32bdbe",
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    
    print(resposta.json())  # Mantém o print original
    return dados  # Retorna os dados para uso em receitaComIngredientes

def receitaComIngredientes(ingredientes, numero):
    tag = ", ".join(ingredientes) #join coloca os elemntos de uma string numa lista separadas por delimitador
    query = {"ingredients": tag, "number":str(numero)}
    response = requests.get(url, headers=headers, params=query)
    receitas = response.json()
    for receita in receitas:
        print(f"Receita: {receita['title']}")
        print(f"Id:  {receita['id']}")
        dados = informacaoReceita(receita['id'])
        print(f"Link da receita: {dados.get('sourceUrl', 'Link não disponível')}")
        print("------------------------")  # Separador entre receitas

def receitaPassoAPasso(id):
    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/analyzedInstructions"
    querystring = {"stepBreakdown":"true"}
    
    headers = {
        "x-rapidapi-key": "2ed4484312mshe3540b669887063p1f94ddjsnb3635e32bdbe",
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    print(response.json())

def main():
    dieta, ingredientes, restricao = escolherDieta()
    receitaComIngredientes(ingredientes, 1)

main()
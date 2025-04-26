import requests

# Variaveis globais
# Spoonacular API
url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api = "2ed4484312mshe3540b669887063p1f94ddjsnb3635e32bdbe"
headers = {
    "x-rapidapi-key" : api,
    "x-rapidapi-host" : "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def escolherDieta():
    ingredientes = []
    restricao_dieta = []

    dieta = input("Que tipo de dieta pretendes seguir? ")

    escolha_ingredientes = input("Desejas usar algum ingrediente especifio (sim/nao)? ").lower() #Lower para nao ter problema de capitalizacao
    while escolha_ingredientes == "sim":
        ingredientes.append(input("Que ingrediente pretendes utilizar: ").lower()) #Damos lower para nao ter problemas na query da api
        escolha_ingredientes = input("Desejas usar algum outro ingrediente (sim/nao)? ").lower()
    
    escolha_restricao = input("Tens alguma restricao dietetica (sim/nao)? ")
    while escolha_restricao == "sim":
        restricao_dieta.append(input("Que restricao dietetica tens? ").lower()) 
        escolha_restricao = input("Desejas adicionar alguma outra restricao (sim/nao)? ").lower()

    return dieta, ingredientes, restricao_dieta

def receitaPassoAPasso(id):
    url = f"{url_base}/recipes/{id}/analyzedInstructions"
    resposta = requests.get(url, headers=headers)
    instrucoes = resposta.json() # retorna lista 
    
    if instrucoes:
        for passo in instrucoes[0]['steps']: # Primeiro dicionario da lista e queremos ver a chave steps
            print(f"Passo {passo['number']}: {passo['step']}")
    else:
        print("Não foram encontradas instruções para esta receita.")


def receitaComIngredientes(ingredientes, numero):
    ingredientes_formatado = ",".join(ingredientes) # join faz com que os elementos de uma lista sejam concatenados com a string que escolhemos
    url = f"{url_base}/recipes/findByIngredients"
    # TEM DE SER DICT!
    query = {"ingredients": ingredientes_formatado, "number":str(numero)}
    resposta = requests.get(url,headers=headers,params=query)
    receitas = resposta.json()
    for receita in receitas:
        print(f"Receita: {receita['title']}")
        print(f"Id: {receita['id']}")
        escolha = input("Desejas ver o passo a passo desta receita (sim/nao)? ").lower()
        if escolha == 'sim':
            receitaPassoAPasso(receita['id'])

def main():
    dieta, ingredientes, restricao_dieta = escolherDieta()
    receitaComIngredientes(ingredientes,1)

main()
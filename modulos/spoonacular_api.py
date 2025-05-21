import os
import requests
from flask import request

url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api = os.getenv('RAPIDAPI_KEY')
headers = {
        "x-rapidapi-key" : api,
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}


def configurar_spoonacular():
    api = os.getenv('RAPIDAPI_KEY')
    headers = {
        "x-rapidapi-key" : api,
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def buscar_receita_spoonacular():
    pesquisa = request.form.get('pesquisa', '')
    dieta = request.form.get('dieta', '')
    ingredientes = request.form.get('ingredientes', '')
    restricoes = request.form.get('restricoes', '')
    numero = int(request.form.get('numero', 5))

    ingredientes_formatado = ingredientes.replace(' ', '').lower() if ingredientes else ''
    restricoes_formatado = restricoes.replace(' ', '').lower() if restricoes else ''

    url = f"{url_base}/recipes/complexSearch"

    query = {
        "query" : pesquisa,
        "diet" : dieta,
        "intolerances" : restricoes_formatado,
        "includeIngredients" : ingredientes_formatado,
        "number" : numero
    }

    resposta = requests.get(url, headers=headers, params=query)
    receitas = resposta.json().get("results", [])

    return receitas

def instrucoes_spoonacular(id):
    url = f"{url_base}/recipes/{id}/information"
    resposta = requests.get(url, headers=headers)
    receita = resposta.json()

    url_instrucoes = f"{url_base}/recipes/{id}/analyzedInstructions"
    resposta_instrucoes = requests.get(url_instrucoes, headers=headers)
    instrucoes = resposta_instrucoes.json()

    return receita, instrucoes

def buscar_receitas_ingredientes_spoonacular():
    ingredientes = request.form.get('ingredientes', '')
    numero = int(request.form.get('numero', 5))

    ingredientes_formatado = ingredientes.replace(' ', '') if ingredientes else ''

    url = f"{url_base}/recipes/findByIngredientes"
    query = {
        "ingredients" : ingredientes_formatado,
        "number" : numero
    }
    resposta = requests.get(url, headers=headers, params=query)
    receitas = resposta.json()

    return receitas

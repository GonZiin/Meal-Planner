import os
import requests
import json
from flask import request

url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api = os.getenv('RAPIDAPI_KEY')
headers = {
    "x-rapidapi-key": api,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def configurar_spoonacular():
    """Atualiza as configurações da API com base nas variáveis de ambiente atuais."""
    global api, headers
    api = os.getenv('RAPIDAPI_KEY')
    headers = {
        "x-rapidapi-key": api,
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    return headers

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
        "query": pesquisa,
        "diet": dieta,
        "intolerances": restricoes_formatado,
        "includeIngredients": ingredientes_formatado,
        "number": numero
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
    
    ingredientes_formatado = ingredientes.replace(' ', '').lower() if ingredientes else ''
    
    url = f"{url_base}/recipes/findByIngredients"  # Corrigido: ingredients em vez de ingredientes
    query = {
        "ingredients": ingredientes_formatado,
        "number": numero
    }
    
    resposta = requests.get(url, headers=headers, params=query)
    receitas = resposta.json()
    return receitas

def gerar_plano_receitas_spoonacular_dia():
    dieta = request.form.get('dieta', '')
    excluidos = request.form.get('excluidos', '')
    tempo = request.form.get('tempo', 'week')
    calorias = request.form.get('calorias', '2000')

    url = f"{url_base}/recipes/mealplans/generate"
    query = {
        "timeFrame": tempo,
        "targetCalories": calorias,
        "diet": dieta,
        "exclude": excluidos
    }

    resposta = requests.get(url, headers=headers, params=query)
    plano = resposta.json()

    return plano, calorias, tempo 

    
def gerar_plano_receitas_spoonacular_semanal(plano):
    for item in plano.get('items', []):
        if 'value' in item and isinstance(item['value'], str):
            try:
                item['value'] = json.loads(item['value'])
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")

import os
import requests
import json
from flask import request
import random

url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api_key = os.getenv('RAPIDAPI_KEY')
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

def configurar_spoonacular():
    global api_key, headers
    api_key = os.getenv('RAPIDAPI_KEY')
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def procurar_receita_spoonacular():
    pesquisa = request.form.get('pesquisa', '')
    dieta = request.form.get('dieta', '')
    ingredientes = request.form.get('ingredientes', '')
    restricoes = request.form.get('restricoes', '')
    numero = int(request.form.get('numero', 5))
    
    url = f"{url_base}/recipes/complexSearch"
    query = {
        "query": pesquisa,
        "diet": dieta,
        "intolerances": restricoes,
        "includeIngredients": ingredientes,
        "number": numero
    }
    resposta = requests.get(url, headers=headers, params=query)
    return resposta.json().get("results", [])

def instrucoes_spoonacular(id_receita):
    info_url = f"{url_base}/recipes/{id_receita}/information"
    instr_url = f"{url_base}/recipes/{id_receita}/analyzedInstructions"
    receita = requests.get(info_url, headers=headers).json()
    instrucoes = requests.get(instr_url, headers=headers).json()
    return receita, instrucoes

def procurar_receitas_ingredientes_spoonacular():
    ingredientes = request.form.get('ingredientes', '')
    numero = int(request.form.get('numero', 5))
    url = f"{url_base}/recipes/findByIngredients"
    query = {"ingredients": ingredientes, "number": numero}
    resposta = requests.get(url, headers=headers, params=query)
    return resposta.json()

def gerar_plano_receitas_spoonacular_dia():
    dieta = request.form.get('dieta', '')
    excluidos = request.form.get('excluidos', '')
    tempo = request.form.get('tempo', 'day')
    calorias = int(request.form.get('calorias', '2000'))
    url = f"{url_base}/recipes/mealplans/generate"
    params = {"timeFrame": tempo, "targetCalories": calorias}
    if dieta:
        params["diet"] = dieta
    if excluidos:
        params["exclude"] = excluidos
    resposta = requests.get(url, headers=headers, params=params)
    plano = resposta.json()
    if tempo == 'day':
        plano_retorno = plano
    else:
        items = []
        pos = 0
        for item in plano['items']:
            valor = json.loads(item['value'])
            refeicao = {
                'id': valor.get('id', 0),
                'title': valor.get('title', 'Sem título'),
                'imageType': valor.get('imageType', 'jpg'),
                'readyInMinutes': 0,
                'servings': 0,
                'sourceUrl': f"https://spoonacular.com/recipes/{valor.get('title', '').replace(' ', '-')}-{valor.get('id', '')}"
            }
            items.append({
                "day": item.get('day', 0),
                "slot": item.get('slot', 0),
                "position": pos,
                "value": refeicao
            })
            pos += 1
        plano_retorno = {"items": items}
    return {"plano": plano_retorno, "parametros": {"dieta": dieta, "excluidos": excluidos, "calorias": calorias, "tempo": tempo}}

def procurar_receita_aleatoria_spoonacular(dieta, excluidos, calorias):
    url = f"{url_base}/recipes/complexSearch"
    params = {
        "diet": dieta,
        "excludeIngredients": excluidos,
        "maxCalories": int(calorias * 1.2),
        "number": 100,
        "sort": "random",
        "sortDirection": "asc"
    }
    resposta = requests.get(url, headers=headers, params=params)
    resultados = resposta.json().get('results', [])
    return random.choice(resultados) if resultados else None

def substituir_receita_no_plano(plano, id_receita_antiga, dieta, excluidos, calorias, tempo):
    if 'meals' in plano:
        for refeicao in plano['meals']:
            if refeicao['id'] == id_receita_antiga:
                nova_receita = procurar_receita_aleatoria_spoonacular(dieta, excluidos, calorias)
                refeicao['id'] = nova_receita['id']
                refeicao['title'] = nova_receita['title']
                refeicao['imageType'] = nova_receita.get('imageType', 'jpg')
                refeicao['sourceUrl'] = f"https://spoonacular.com/recipes/{nova_receita['title'].replace(' ', '-')}-{nova_receita['id']}"
                break
    else:
        for item in plano['items']:
            if item['value']['id'] == id_receita_antiga:
                nova_receita = procurar_receita_aleatoria_spoonacular(dieta, excluidos, calorias)
                item['value'] = {
                    'id': nova_receita['id'],
                    'title': nova_receita['title'],
                    'imageType': nova_receita.get('imageType', 'jpg'),
                    'readyInMinutes': 0,
                    'servings': 0,
                    'sourceUrl': f"https://spoonacular.com/recipes/{nova_receita['title'].replace(' ', '-')}-{nova_receita['id']}"
                }
                break
    return plano

def gerar_plano_receitas_spoonacular_semanal(plano):
    return plano

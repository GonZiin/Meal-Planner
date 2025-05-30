import os
import requests
from flask import request

url_base = "https://themealdb.p.rapidapi.com"
api = os.getenv('THEMEALDB_KEY')
headers = {
    "x-rapidapi-key": api,
    "x-rapidapi-host": "themealdb.p.rapidapi.com"   
}

def configurar_themealdb():
    global api, headers
    api = os.getenv('THEMEALDB_KEY')
    headers = {
        "x-rapidapi-key": api,
        "x-rapidapi-host": "themealdb.p.rapidapi.com"
    }
    return headers

def procurar_receita_themealdb():
    pesquisa = request.form.get('pesquisa', '')
    
    numero_receitas = int(request.form.get('numero', 5))
    
    url = f"{url_base}/search.php"
    query = {
        "s": pesquisa
    }
    resposta = requests.get(url, headers=headers, params=query)
    
    todas_receitas = resposta.json().get("meals", [])
    return todas_receitas[:numero_receitas]

def instrucoes_themealdb(id):
    url = f"{url_base}/lookup.php"
    query = {
        "i": id
    }
    resposta = requests.get(url, headers=headers, params=query)
    receita = resposta.json().get("meals", [])
    return receita[0] if receita else None
import os
import requests
import json
from flask import request

# Configurações da API
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
    print(f"API Key configurada: {'Sim' if api else 'Não'}")
    return headers

def _fazer_requisicao_api(url, params=None, timeout=15):
    """Função helper para fazer requisições à API com tratamento de erro melhorado."""
    try:
        print(f"[DEBUG] Fazendo requisição para: {url}")
        print(f"[DEBUG] Parâmetros: {params}")
        print(f"[DEBUG] Headers: {headers}")
        
        resposta = requests.get(url, headers=headers, params=params, timeout=timeout)
        
        print(f"[DEBUG] Status Code: {resposta.status_code}")
        print(f"[DEBUG] Response Headers: {dict(resposta.headers)}")
        
        if resposta.status_code == 404:
            raise Exception(f"Endpoint não encontrado (404). URL: {url}")
        elif resposta.status_code == 401:
            raise Exception("Erro de autenticação (401). Verifique sua API key.")
        elif resposta.status_code == 403:
            raise Exception("Acesso negado (403). Verifique as permissões da sua API key.")
        elif resposta.status_code == 429:
            raise Exception("Limite de requisições excedido (429). Tente novamente mais tarde.")
        elif resposta.status_code >= 400:
            raise Exception(f"Erro HTTP {resposta.status_code}: {resposta.text}")
        
        return resposta.json()
        
    except requests.exceptions.Timeout:
        raise Exception("Timeout na requisição à API. Tente novamente.")
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão com a API. Verifique sua internet.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de requisição: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Resposta da API não é um JSON válido")

def buscar_receita_spoonacular():
    try:
        if not api:
            raise Exception("API Key do Spoonacular não configurada. Verifique a variável RAPIDAPI_KEY no arquivo .env")
        
        pesquisa = request.form.get('pesquisa', '')
        dieta = request.form.get('dieta', '')
        ingredientes = request.form.get('ingredientes', '')
        restricoes = request.form.get('restricoes', '')
        numero = int(request.form.get('numero', 5))
        
        if not any([pesquisa, dieta, ingredientes, restricoes]):
            raise Exception("Por favor, forneça pelo menos um critério de busca")
        
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
        
        # Remove parâmetros vazios
        query = {k: v for k, v in query.items() if v}
        
        data = _fazer_requisicao_api(url, query)
        receitas = data.get("results", [])
        
        print(f"[INFO] Encontradas {len(receitas)} receitas")
        return receitas
        
    except Exception as e:
        raise Exception(f"Erro ao buscar receitas: {str(e)}")

def instrucoes_spoonacular(id):
    try:
        if not api:
            raise Exception("API Key do Spoonacular não configurada")
            
        url = f"{url_base}/recipes/{id}/information"
        receita = _fazer_requisicao_api(url)
        
        url_instrucoes = f"{url_base}/recipes/{id}/analyzedInstructions"
        try:
            instrucoes = _fazer_requisicao_api(url_instrucoes)
        except Exception as e:
            print(f"[WARNING] Erro ao buscar instruções: {e}")
            instrucoes = []
        
        return receita, instrucoes
        
    except Exception as e:
        raise Exception(f"Erro ao buscar detalhes da receita: {str(e)}")

def buscar_receitas_ingredientes_spoonacular():
    try:
        if not api:
            raise Exception("API Key do Spoonacular não configurada")
            
        ingredientes = request.form.get('ingredientes', '')
        numero = int(request.form.get('numero', 5))
        
        if not ingredientes:
            raise Exception("Por favor, forneça pelo menos um ingrediente")
        
        ingredientes_formatado = ingredientes.replace(' ', '').lower()
        
        url = f"{url_base}/recipes/findByIngredients"
        query = {
            "ingredients": ingredientes_formatado,
            "number": numero
        }
        
        receitas = _fazer_requisicao_api(url, query)
        return receitas
        
    except Exception as e:
        raise Exception(f"Erro ao buscar receitas por ingredientes: {str(e)}")

def gerar_plano_receitas_spoonacular_dia():
    try:
        if not api:
            raise Exception("API Key do Spoonacular não configurada")
            
        dieta = request.form.get('dieta', '')
        excluidos = request.form.get('excluidos', '')
        tempo = request.form.get('tempo', 'day')
        calorias = request.form.get('calorias', '2000')

        # Diferentes endpoints baseados no tempo
        if tempo == 'day':
            url = f"{url_base}/mealplanner/generate"
            query = {
                "timeFrame": "day",
                "targetCalories": calorias
            }
            
            # Adiciona parâmetros opcionais apenas se fornecidos
            if dieta:
                query["diet"] = dieta
            if excluidos:
                query["exclude"] = excluidos
                
        elif tempo == 'week':
            # Para plano semanal, usa endpoint diferente
            url = f"{url_base}/mealplanner/generate"
            query = {
                "timeFrame": "week",
                "targetCalories": calorias
            }
            
            if dieta:
                query["diet"] = dieta
            if excluidos:
                query["exclude"] = excluidos
        else:
            raise Exception("Tipo de plano inválido. Use 'day' ou 'week'")

        print(f"[DEBUG] Gerando plano para: {tempo}")
        print(f"[DEBUG] Query parameters: {query}")
        
        plano = _fazer_requisicao_api(url, query)
        
        # Verifica se o plano foi gerado corretamente
        if not plano:
            raise Exception("Plano vazio retornado pela API")
            
        return plano, calorias, tempo
        
    except Exception as e:
        # Se o endpoint principal falhar, tenta método alternativo
        if "404" in str(e):
            try:
                return _gerar_plano_alternativo(tempo, calorias, dieta, excluidos)
            except Exception as fallback_error:
                raise Exception(f"Erro no método principal: {str(e)}. Método alternativo também falhou: {str(fallback_error)}")
        else:
            raise Exception(f"Erro ao gerar plano de refeições: {str(e)}")

def _gerar_plano_alternativo(tempo, calorias, dieta, excluidos):
    """Método alternativo para gerar plano de refeições usando busca de receitas."""
    try:
        print("[INFO] Tentando método alternativo para gerar plano")
        
        # Calcular calorias por refeição
        calorias_int = int(calorias)
        if tempo == 'day':
            # 3 refeições por dia
            calorias_por_refeicao = calorias_int // 3
            num_receitas = 3
        else:
            # 7 dias x 3 refeições = 21 receitas
            calorias_por_refeicao = calorias_int // 3
            num_receitas = 21
        
        # Buscar receitas usando complexSearch
        url = f"{url_base}/recipes/complexSearch"
        query = {
            "number": num_receitas,
            "maxCalories": calorias_por_refeicao + 200,  # Margem de erro
            "minCalories": max(100, calorias_por_refeicao - 200),
            "addRecipeInformation": True,
            "fillIngredients": True
        }
        
        if dieta:
            query["diet"] = dieta
        if excluidos:
            query["excludeIngredients"] = excluidos
        
        data = _fazer_requisicao_api(url, query)
        receitas = data.get("results", [])
        
        if not receitas:
            raise Exception("Nenhuma receita encontrada para os critérios especificados")
        
        # Formatar como plano de refeições
        if tempo == 'day':
            plano = {
                "meals": receitas[:3],
                "nutrients": {
                    "calories": sum(r.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", 0) for r in receitas[:3] if r.get("nutrition")),
                    "protein": 0,
                    "fat": 0,
                    "carbohydrates": 0
                }
            }
        else:
            # Plano semanal
            items = []
            for i, receita in enumerate(receitas[:21], 1):
                items.append({
                    "day": ((i-1) // 3) + 1,
                    "slot": (i-1) % 3 + 1,
                    "position": i-1,
                    "type": "RECIPE",
                    "value": receita
                })
            
            plano = {"items": items}
        
        print(f"[INFO] Plano alternativo gerado com {len(receitas)} receitas")
        return plano, calorias, tempo
        
    except Exception as e:
        raise Exception(f"Método alternativo falhou: {str(e)}")

def gerar_plano_receitas_spoonacular_semanal(plano):
    """Processa dados do plano semanal."""
    try:
        if not plano or 'items' not in plano:
            print("[WARNING] Plano semanal vazio ou inválido")
            return
            
        for item in plano.get('items', []):
            if 'value' in item:
                # Se value é string, tenta decodificar JSON
                if isinstance(item['value'], str):
                    try:
                        item['value'] = json.loads(item['value'])
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Erro ao decodificar JSON do item: {e}")
                        # Mantém como string se não conseguir decodificar
                        
                # Adiciona informações de dia se não existir
                if 'day' not in item:
                    # Calcula o dia baseado na posição
                    position = item.get('position', 0)
                    item['day'] = (position // 3) + 1
                    
        print(f"[INFO] Processados {len(plano.get('items', []))} itens do plano semanal")
        
    except Exception as e:
        print(f"[ERROR] Erro ao processar plano semanal: {e}")

def testar_conexao_api():
    """Função para testar a conectividade com a API."""
    try:
        if not api:
            return False, "API Key não configurada"
        
        # Testa com uma busca simples
        url = f"{url_base}/recipes/complexSearch"
        query = {"query": "chicken", "number": 1}
        
        _fazer_requisicao_api(url, query)
        return True, "Conexão com API funcionando"
        
    except Exception as e:
        return False, f"Erro na conexão: {str(e)}"
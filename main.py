import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_temporaria") 

url_base = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api = os.getenv("RAPIDAPI_KEY")
headers = {
    "x-rapidapi-key": api,
    "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar-receita', methods=['GET'])
def mostrar_busca_receita():
    return render_template('buscar_receita.html')

@app.route('/buscar-receita', methods=['POST'])
def processar_busca_receita():
    try:
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
        
        return render_template('resultados_busca.html', receitas=receitas)
    
    except Exception as e:
        flash(f"Erro ao buscar receitas: {str(e)}")
        return redirect(url_for('mostrar_busca_receita'))

@app.route('/receita/<int:id>')
def mostrar_receita(id):
    try:
        url = f"{url_base}/recipes/{id}/information"
        resposta = requests.get(url, headers=headers)
        receita = resposta.json()
        
        url_instrucoes = f"{url_base}/recipes/{id}/analyzedInstructions"
        resposta_instrucoes = requests.get(url_instrucoes, headers=headers)
        instrucoes = resposta_instrucoes.json()
        
        return render_template('receita_detalhes.html', receita=receita, instrucoes=instrucoes)
    
    except Exception as e:
        flash(f"Erro ao carregar detalhes da receita: {str(e)}")
        return redirect(url_for('index'))

@app.route('/receitas-por-ingredientes', methods=['GET'])
def mostrar_busca_ingredientes():
    return render_template('buscar_por_ingredientes.html')

@app.route('/receitas-por-ingredientes', methods=['POST'])
def processar_busca_ingredientes():
    try:
        ingredientes = request.form.get('ingredientes', '')
        numero = int(request.form.get('numero', 5))
        
        ingredientes_formatado = ingredientes.replace(' ', '').lower() if ingredientes else ''
        
        url = f"{url_base}/recipes/findByIngredients"
        query = {"ingredients": ingredientes_formatado, "number": numero}
        resposta = requests.get(url, headers=headers, params=query)
        receitas = resposta.json()
        
        return render_template('resultados_ingredientes.html', receitas=receitas)
    
    except Exception as e:
        flash(f"Erro ao buscar receitas por ingredientes: {str(e)}")
        return redirect(url_for('mostrar_busca_ingredientes'))

@app.route('/plano-refeicoes', methods=['GET'])
def mostrar_form_plano():
    return render_template('plano_refeicoes_form.html')

@app.route('/plano-refeicoes', methods=['POST'])
def gerar_plano_refeicoes():
    try:
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
        
        resposta.raise_for_status()
        
        plano = resposta.json()
        
        if 'items' not in plano or not isinstance(plano['items'], list):
            flash("A API retornou dados em formato inesperado.")
            return redirect(url_for('mostrar_form_plano'))
            
        for item in plano['items']:
            if 'value' in item and isinstance(item['value'], str):
                try:
                    item['value'] = json.loads(item['value'])
                except json.JSONDecodeError:
                    item['value'] = {
                        'id': 0,
                        'title': "Refeição não identificada",
                        'imageType': 'jpg'
                    }
            
            if 'day' in item and not isinstance(item['day'], int):
                try:
                    item['day'] = int(item['day'])
                except (ValueError, TypeError):
                    item['day'] = 1  
                    
            if 'slot' in item and not isinstance(item['slot'], int):
                try:
                    item['slot'] = int(item['slot'])
                except (ValueError, TypeError):
                    item['slot'] = 1  

        return render_template('plano_refeicoes_resultado.html', plano=plano)
        
    except requests.exceptions.RequestException as e:
        flash(f"Erro na comunicação com a API: {str(e)}")
        return redirect(url_for('mostrar_form_plano'))
    except Exception as e:
        flash(f"Erro ao gerar plano de refeições: {str(e)}")
        return redirect(url_for('mostrar_form_plano'))


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form['nome']
        peso = float(request.form['peso'])
        altura_cm = float(request.form['altura'])
        calorias = int(request.form['calorias'])
        dieta = request.form['dieta']
        avatar = request.form.get('avatar', '1')

        # Calcular IMC
        altura_m = altura_cm / 100
        bmi = round(peso / (altura_m ** 2), 1)

        # Determinar status do IMC
        if bmi < 18.5:
            bmi_status = "Abaixo do peso"
        elif 18.5 <= bmi < 25:
            bmi_status = "Peso normal"
        elif 25 <= bmi < 30:
            bmi_status = "Sobrepeso"
        else:
            bmi_status = "Obesidade"

        # Guardar todos os dados na sessão
        session['user_name'] = nome
        session['peso'] = peso
        session['altura'] = altura_cm
        session['calorias'] = calorias
        session['dieta'] = dieta
        session['avatar'] = avatar
        session['bmi'] = bmi
        session['bmi_status'] = bmi_status

        # Redirecionar para a mesma página para evitar reenvio do formulário
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('perfil'))

    # GET - Recuperar dados da sessão
    user_name = session.get('user_name', 'Utilizador')
    peso = session.get('peso', '')
    altura = session.get('altura', '')
    calorias = session.get('calorias', '')
    dieta = session.get('dieta', '')
    avatar = session.get('avatar', '1')
    bmi = session.get('bmi')
    bmi_status = session.get('bmi_status')

    return render_template('perfil.html', 
                           user_name=user_name,
                           peso=peso,
                           altura=altura,
                           calorias=calorias,
                           dieta=dieta,
                           avatar=avatar,
                           bmi=bmi,
                           bmi_status=bmi_status)




if __name__ == '__main__':
    app.run(debug=True)

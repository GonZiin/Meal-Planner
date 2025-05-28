from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from modulos import spoonacular_api, utils, themealdb_api
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_temporaria")

# Configurar ambas as APIs
spoonacular_api.configurar_spoonacular()
themealdb_api.configurar_themealdb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar-receita', methods=['GET'])
def mostrar_busca_receita():
    return render_template('buscar_receita.html')

@app.route('/buscar-receita', methods=['POST'])
def processar_busca_receita():
    try:
        api_escolhida = request.form.get('api', 'spoonacular')  
        
        if api_escolhida == 'themealdb':
            resposta = themealdb_api.buscar_receita_themealdb()
        else:
            resposta = spoonacular_api.buscar_receita_spoonacular()
            
        return render_template('resultados_busca.html', receitas=resposta, api_usada=api_escolhida)
    except Exception as e:
        flash(f"Erro ao buscar receitas: {str(e)}")
        return redirect(url_for('mostrar_busca_receita'))

@app.route('/receita/<int:id>')
def mostrar_receita(id):
    try:
        receita, instrucoes = spoonacular_api.instrucoes_spoonacular(id)
        return render_template('receita_detalhes.html', receita=receita, instrucoes=instrucoes)
    except Exception as e:
        flash(f"Erro ao carregar detalhes da receita: {str(e)}")
        return redirect(url_for('index'))

@app.route('/receita-mealdb/<meal_id>')
def mostrar_receita_mealdb(meal_id):
    try:
        receita = themealdb_api.instrucoes_themealdb(meal_id)
        return render_template('receita_detalhes_mealdb.html', receita=receita)
    except Exception as e:
        flash(f"Erro ao carregar detalhes da receita: {str(e)}")
        return redirect(url_for('index'))

@app.route('/receitas-por-ingredientes', methods=['GET'])
def mostrar_busca_ingredientes():
    return render_template('buscar_por_ingredientes.html')

@app.route('/receitas-por-ingredientes', methods=['POST'])
def processar_busca_ingredientes():
    try:
        receitas = spoonacular_api.buscar_receitas_ingredientes_spoonacular()
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
        plano, calorias, tempo = spoonacular_api.gerar_plano_receitas_spoonacular_dia()
        if tempo == 'day':
            return render_template('plano_dia.html', plano=plano, calorias=calorias)
        elif tempo == 'week':
            spoonacular_api.gerar_plano_receitas_spoonacular_semanal(plano)
            return render_template('plano_semana.html', plano=plano)
    except Exception as e:
        flash(f"Erro ao gerar plano de refeições: {str(e)}")
        return redirect(url_for('mostrar_form_plano'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        utils.perfil_setup()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('perfil'))
    if request.method == 'GET':
        user_name, peso, altura, calorias, dieta, avatar, bmi, bmi_status = utils.perfil_recuperar_dados()
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

from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
from modulos import spoonacular_api, utils, themealdb_api
from weasyprint import HTML
import os
import json

load_dotenv()
app = Flask(__name__)

spoonacular_api.configurar_spoonacular()
themealdb_api.configurar_themealdb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procurar-receita', methods=['GET'])
def mostrar_busca_receita():
    return render_template('procurar_receita.html')

@app.route('/procurar-receita', methods=['POST'])
def processar_busca_receita():
    api_escolhida = request.form.get('api', 'spoonacular')  
    
    if api_escolhida == 'themealdb':
        resposta = themealdb_api.procurar_receita_themealdb()
    else:
        resposta = spoonacular_api.procurar_receita_spoonacular()
        
    return render_template('resultados_pesquisa.html', receitas=resposta, api_usada=api_escolhida)

@app.route('/receita/<int:id>')
def mostrar_receita(id):
    receita, instrucoes = spoonacular_api.instrucoes_spoonacular(id)
    return render_template('receita_detalhes.html', receita=receita, instrucoes=instrucoes)

@app.route('/receita-mealdb/<meal_id>')
def mostrar_receita_mealdb(meal_id):
    receita = themealdb_api.instrucoes_themealdb(meal_id)
    return render_template('receita_detalhes_mealdb.html', receita=receita)

@app.route('/receitas-por-ingredientes', methods=['GET'])
def mostrar_busca_ingredientes():
    return render_template('procurar_por_ingredientes.html')

@app.route('/receitas-por-ingredientes', methods=['POST'])
def processar_busca_ingredientes():
    receitas = spoonacular_api.procurar_receitas_ingredientes_spoonacular()
    return render_template('resultados_ingredientes.html', receitas=receitas)

@app.route('/plano-refeicoes', methods=['GET', 'POST'])
def plano_refeicoes():
    if request.method == 'GET':
        return render_template('plano_refeicoes_form.html')
    
    resultado = spoonacular_api.gerar_plano_receitas_spoonacular_dia()
    plano = resultado["plano"]
    parametros = resultado["parametros"]
    calorias = parametros["calorias"]
    tempo = parametros["tempo"]

    if tempo == 'day':
        return render_template('plano_dia.html', plano=plano, parametros=parametros, calorias=calorias)
    elif tempo == 'week':
        spoonacular_api.gerar_plano_receitas_spoonacular_semanal(plano)
        return render_template('plano_semana.html', plano=plano, parametros=parametros)
    
@app.route('/receitas')
def mostrar_receitas():
    receitas = session.get('receitas_anteriores', [])
    api_usada = session.get('api_usada', 'spoonacular')
    return render_template('resultados_pesquisa.html', receitas=receitas, api_usada=api_usada)


@app.route('/substituir_receita', methods=['POST'])
def substituir_receita():
    plano_json = request.form['plano']
    parametros_json = request.form['parametros']
    id_receita = request.form['id_receita']
    
    plano = json.loads(plano_json)
    parametros = json.loads(parametros_json)
    
    novo_plano = spoonacular_api.substituir_receita_no_plano(
        plano=plano,
        id_receita_antiga=int(id_receita),
        dieta=parametros['dieta'],
        excluidos=parametros['excluidos'],
        calorias=parametros['calorias'],
        tempo=parametros['tempo']
    )
    
    if parametros['tempo'] == 'day':
        return render_template('plano_dia.html', plano=novo_plano, parametros=parametros, calorias=parametros['calorias'])
    else:
        return render_template('plano_semana.html', plano=novo_plano, parametros=parametros)


@app.route('/baixar_plano', methods=['POST'])
def baixar_plano():
    plano_json = request.form['plano']
    parametros_json = request.form.get('parametros', '{}')
    
    pdf = utils.gerar_pdf_plano(plano_json, parametros_json)
    
    resposta = make_response(pdf)
    resposta.headers['Content-Type'] = 'application/pdf'
    resposta.headers['Content-Disposition'] = 'attachment; filename=plano_alimentar.pdf'
    return resposta

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        utils.perfil_setup()
        return redirect(url_for('perfil'))
    
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

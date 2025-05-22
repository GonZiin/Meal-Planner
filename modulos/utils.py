from flask import request, session  

def perfil_setup():
    nome = request.form['nome']
    peso = float(request.form['peso'])
    altura_cm = float(request.form['altura'])
    calorias = int(request.form['calorias'])
    dieta = request.form['dieta']
    avatar = request.form.get('avatar', 1)

    altura_m = altura_cm / 100
    bmi = round(peso / (altura_m ** 2), 1)

    if bmi < 18.5:
        bmi_status = "Abaixo do peso"
    elif 18.5 <= bmi < 25:
        bmi_status = "Peso normal"
    elif 25 <= bmi < 30:
        bmi_status = "Sobrepeso"
    else:
        bmi_status = "Obesidade"

    session['user_name'] = nome
    session['peso'] = peso
    session['altura'] = altura_cm
    session['calorias'] = calorias
    session['dieta'] = dieta
    session['avatar'] = avatar
    session['bmi'] = bmi
    session['bmi_status'] = bmi_status

def perfil_recuperar_dados():
    user_name = session.get('user_name', 'Utilizador')
    peso = session.get('peso', '')
    altura = session.get('altura', '')
    calorias = session.get('calorias', '')
    dieta = session.get('dieta', '')
    avatar = session.get('avatar', '1')
    bmi = session.get('bmi')
    bmi_status = session.get('bmi_status')

    return user_name, peso, altura, calorias, dieta, avatar, bmi, bmi_status

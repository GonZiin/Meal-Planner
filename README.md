Claro! Aqui está o README simplificado em formato Markdown (.md):

````md
# Meal Planner

Aplicação web em Flask para gerar planos de refeições personalizados usando a API Spoonacular.

---

## Funcionalidades

- Criação de perfil com dados pessoais e objetivos calóricos  
- Geração de planos de refeições diários e semanais  
- Pesquisa de receitas por ingredientes e tipo de dieta  
- Informações nutricionais detalhadas  

---

## Requisitos

- Python 3.8+  
- Conta na RapidAPI com chave válida para Spoonacular  

---

## Instalação

1. Clonar o repositório:  
   ```bash
   git clone https://github.com/GonZiin/Meal-Planner.git
   cd Meal-Planner
````

2. Criar e ativar ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Instalar dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Criar arquivo `.env` com as variáveis:

   ```
   RAPIDAPI_KEY=sua_chave
   SECRET_KEY=sua_chave_secreta
   FLASK_ENV=development
   ```

---

## Uso

Executar:

```bash
flask run
```

Abrir [http://localhost:5000](http://localhost:5000) no navegador.

---

## Tecnologias

* Python, Flask
* Bootstrap para interface
* Spoonacular API para receitas

---

## Contacto

Gonçalo Gomes – [goncalogomespessoal@outlook.pt](mailto:goncalogomespessoal@outlook.pt)



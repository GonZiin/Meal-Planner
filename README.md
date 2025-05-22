````markdown
# Gerador de Planos de Refeições com Flask & Spoonacular

Projeto desenvolvido em Python no ambito da UC laboratorio de programacao, desenvolvido em Flask e Python
---

## Funcionalidades

- Cadastro de perfil com altura, peso, dieta e calorias desejadas
- Cálculo de IMC (Índice de Massa Corporal)
- Geração de planos de refeição diários ou semanais
- Busca de receitas com base em ingredientes ou restrições
- Interface web simples com Flask
- Integração com a API da Spoonacular

---

## Requisitos

- Python 3.8+
- Conta na [RapidAPI](https://rapidapi.com/) com acesso à Spoonacular
- Ambiente virtual (opcional, mas recomendado)

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
````

---

## Configuração

Crie um ficheiro `.env` com a sua chave de API do RapidAPI:

```env
RAPIDAPI_KEY=sua_chave_aqui
```

---

## Execução

```bash
flask run
```

Depois aceda a: [http://localhost:5000](http://localhost:5000)

---

## 📚 Licença

Distribuído sob a licença MIT. Veja.

---


## 📬 Contacto

Em caso de dúvidas ou sugestões, entre em contacto via [goncalogomespessoal@outlook.pt](goncalogomespessoal@outlook.pt)

```

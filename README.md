# Gerador de Planos de Refeições

**Aplicação web desenvolvida em Flask para geração automática de planos alimentares personalizados**

Projecto académico desenvolvido no âmbito da UC Laboratório de Programação, utilizando Python, Flask e a API Spoonacular para criar planos de refeições adaptados às necessidades individuais de cada utilizador.

---

## Funcionalidades

### Gestão de Perfil
- Registo personalizado com dados antropométricos (altura, peso)
- Configuração de preferências alimentares e tipo de dieta
- Definição de objectivos calóricos diários
- Cálculo automático do IMC com interpretação dos resultados

### Planeamento de Refeições
- Geração de planos diários adaptados ao perfil do utilizador
- Planos semanais completos com variedade nutricional
- Sugestões baseadas em restrições alimentares específicas
- Integração com base de dados nutricional da Spoonacular

### Pesquisa de Receitas
- Busca avançada por ingredientes disponíveis
- Filtros por tipo de dieta (vegetariana, vegana, sem glúten, etc.)
- Informações nutricionais detalhadas
- Tempo de preparação e dificuldade

---

## Requisitos do Sistema

### Software Necessário
- Python 3.8 ou superior
- pip (gestor de pacotes Python)
- Navegador web moderno

### Dependências Externas
- Conta activa na [RapidAPI](https://rapidapi.com/)
- Subscrição da API Spoonacular através da RapidAPI
- Chave de API válida

### Ambiente de Desenvolvimento (Recomendado)
- Ambiente virtual Python (venv)
- Editor de código (VS Code, PyCharm, etc.)

---

## Instalação

### 1. Obter o Código Fonte
```bash
git clone https://github.com/seu-usuario/gerador-planos-refeicoes.git
cd gerador-planos-refeicoes
```

### 2. Configurar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Activar ambiente virtual
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um ficheiro `.env` na raiz do projecto:
```env
RAPIDAPI_KEY=sua_chave_da_rapidapi
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui
```

---

## Configuração da API

### Obter Chave da RapidAPI
1. Registe-se em [RapidAPI](https://rapidapi.com/)
2. Procure pela API "Spoonacular"
3. Subscreva um plano (gratuito disponível)
4. Copie a sua chave de API
5. Adicione a chave ao ficheiro `.env`

### Limites da API Gratuita
A versão gratuita da Spoonacular permite:
- 150 pedidos por dia
- Acesso a funcionalidades básicas
- Informações nutricionais limitadas

---

## Execução

### Modo de Desenvolvimento
```bash
# Certificar que o ambiente virtual está activo
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Executar a aplicação
flask run
```

### Acesso à Aplicação
Abra o navegador e aceda a: [http://localhost:5000](http://localhost:5000)

---

## Estrutura do Projecto

```
gerador-planos-refeicoes/
├── app.py                 # Aplicação principal Flask
├── config.py             # Configurações da aplicação
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (não incluído no git)
├── static/              # Ficheiros estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── perfil.html
│   └── planos.html
└── utils/              # Módulos auxiliares
    ├── api_client.py
    ├── calculations.py
    └── validators.py
```

---

## Utilização

### 1. Criar Perfil
- Aceda à página de registo
- Introduza os seus dados pessoais
- Defina as suas preferências alimentares
- Estabeleça os seus objectivos calóricos

### 2. Gerar Plano de Refeições
- Seleccione o tipo de plano (diário/semanal)
- Escolha as restrições alimentares
- Clique em "Gerar Plano"
- Visualize as sugestões personalizadas

### 3. Explorar Receitas
- Utilize a funcionalidade de pesquisa
- Filtre por ingredientes ou tipo de dieta
- Aceda às informações nutricionais detalhadas

---

## Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem de programação principal
- **Flask** - Framework web minimalista
- **Requests** - Cliente HTTP para consumo de APIs
- **Python-dotenv** - Gestão de variáveis de ambiente

### Frontend
- **HTML5** - Estrutura das páginas web
- **CSS3** - Estilização e layout responsivo
- **JavaScript** - Interactividade do lado do cliente
- **Bootstrap** - Framework CSS para design responsivo

### APIs Externas
- **Spoonacular API** - Base de dados de receitas e informações nutricionais
- **RapidAPI** - Plataforma de gestão de APIs

---

## Desenvolvimento e Contribuições

### Configuração para Desenvolvimento
```bash
# Instalar dependências adicionais de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
python -m pytest

# Verificar qualidade do código
flake8 app.py
```

### Directrizes de Contribuição
- Siga as convenções PEP 8 para código Python
- Documente todas as funções e classes
- Inclua testes para novas funcionalidades
- Mantenha o README actualizado

---

## Resolução de Problemas

### Problemas Comuns

**Erro de Chave API Inválida**
- Verifique se a chave está correcta no ficheiro `.env`
- Confirme que a subscrição da Spoonacular está activa

**Erro de Dependências**
- Certifique-se de que o ambiente virtual está activo
- Reinstale as dependências: `pip install -r requirements.txt`

**Problemas de Conectividade**
- Verifique a ligação à internet
- Confirme se a API Spoonacular está operacional

---

## Licença

Este projecto está licenciado sob a Licença MIT. Consulte o ficheiro `LICENSE` para mais detalhes.

---

## Contacto

**Desenvolvedor**: Gonçalo Gomes  
**Email**: [goncalogomespessoal@outlook.pt](mailto:goncalogomespessoal@outlook.pt)  
**Universidade**: [UTAD]  
**Curso**: [Engenharia Informática]

Para questões técnicas, sugestões de melhoria ou reportar problemas, não hesite em entrar em contacto.

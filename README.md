# 📚 Agno Estudos - Playground de Agentes AI

> Uma coleção de agentes AI inteligentes construídos com o framework **Agno** e modelos **Groq**

## 🌟 Visão Geral

Este projeto demonstra o poder dos agentes AI modernos através de implementações práticas usando o framework Agno. Inclui desde assistentes especializados até sistemas multi-agentes colaborativos.

## 🤖 Agentes Disponíveis

### 📖 Biblioteca Assistant (meio instável, tem que ser meio especifíco pra funcionar)
Um assistente bibliotecário inteligente com acesso a um banco de dados de livros.

**Características:**
- 🔍 Consultas SQL inteligentes
- 📊 Análise de dados de livros
- 💬 Interface conversacional
- 🗄️ Integração com SQLite

**Exemplo de uso:**
```
"Mostre-me os 5 livros mais antigos da biblioteca"
"Quais autores têm mais de 3 livros?"
"Qual é a média de avaliação dos livros de ficção?"
```

### 🌐 Multi-Agent System
Sistema colaborativo com agentes especializados para análise financeira.

**Agentes:**
- **🔍 Web Agent**: Busca informações e notícias em tempo real
- **📈 Financial Agent**: Análise de dados financeiros e mercado

**Capacidades:**
- Pesquisa web com DuckDuckGo
- Análise de ações com Yahoo Finance
- Relatórios colaborativos
- Dados em tabelas formatadas

## 🚀 Como Executar

### Pré-requisitos
- Python 3.12+
- Chave API do Groq
- Docker (opcional)

### 🐍 Execução Local

1. **Clone o repositório**
```bash
git clone https://github.com/samuell19/agno-estudos.git
cd agno-estudos/finanças
```

2. **Instale as dependências**
```bash
pip install agno groq sqlalchemy rich
```

3. **Configure sua API key**
```bash
export GROQ_API_KEY="sua-chave-groq-aqui"
```

4. **Execute o assistente da biblioteca**
```bash
python biblioteca.py
```

5. **Execute o sistema multi-agentes**
```bash
python multi_agent.py
```

6. **Acesse o playground**
```
http://localhost:7777/playground
```

### 🐳 Execução com Docker


1. **Build e execute**
```bash
docker-compose up --build
```

2. **Acesse o playground**
```
http://localhost:7777/playground
```

## 📁 Estrutura do Projeto

```
agno-estudos/
├── finanças/
│   ├── biblioteca.py          # 📚 Assistente bibliotecário
│   ├── multi_agent.py         # 🤖 Sistema multi-agentes
│   ├── agent_memory.py        # 🧠 Sistema de memória
│   ├── web_search_agent.py    # 🔍 Agente de busca web
│   ├── biblioteca.db          # 🗄️ Banco de dados de livros
│   ├── Dockerfile             # 🐳 Configuração Docker
│   ├── docker-compose.yml     # 🐳 Orquestração Docker
│   └── requirements.txt       # 📦 Dependências Python
├── .gitignore                 # 🚫 Arquivos ignorados
└── README.md                  # 📖 Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **[Agno](https://github.com/agno-ai/agno)** - Framework para agentes AI
- **[Groq](https://groq.com/)** - Modelos de linguagem ultrarrápidos
- **SQLite** - Banco de dados embarcado
- **Docker** - Containerização
- **FastAPI** - API web moderna
- **Rich** - Interface de terminal bonita

## 💡 Casos de Uso

### 📚 Biblioteca Assistant
- Gerenciamento de acervo bibliográfico
- Consultas inteligentes sobre livros
- Relatórios automatizados
- Sistema de recomendações

### 📈 Multi-Agent Financial System
- Análise de mercado financeiro
- Pesquisa de notícias de empresas
- Relatórios de investimento
- Monitoramento de ações

## 🎯 Exemplos de Queries

### Para o Biblioteca Assistant:
```
💬 "Liste os livros publicados após 1950"
💬 "Qual autor tem a maior média de avaliação?"
💬 "Mostre estatísticas por gênero literário"
💬 "Quais livros têm mais de 400 páginas?"
```

### Para o Multi-Agent System:
```
💬 "Analise o desempenho das ações de tecnologia"
💬 "Pesquise notícias sobre inteligência artificial"
💬 "Compare o mercado de semicondutores"
💬 "Relatório sobre empresas de energia renovável"
```

## 🔧 Personalização

### Adicionando Novos Agentes
```python
from agno.agent import Agent
from agno.models.groq import Groq

novo_agente = Agent(
    name="Meu Agente",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="Suas instruções aqui",
    tools=[SuasFerramentas()],
    markdown=True,
)
```

### Configurando Ferramentas Personalizadas
```python
from agno.tools.sql import SQLTools

class MinhaFerramentaSQL(SQLTools):
    def schema(self):
        # Customize o schema conforme necessário
        return super().schema()
```

## 🚀 Próximos Passos

- [ ] 🧠 Sistema de memória persistente
- [ ] 📊 Dashboard de métricas
- [ ] 🔄 Agentes com feedback loop
- [ ] 🌐 Integração com mais APIs



# 🚀 Ecossistema de Otimização de Marketing de Direct Response

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.49+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Visão Geral

Este projeto consiste em um **ecossistema de software completo** e de baixo custo para otimizar o marketing de resposta direta, com foco inicial em infoprodutos. A plataforma centraliza a inteligência de mercado, a criação de copy de alta conversão e a geração de produtos digitais, permitindo uma operação ágil, estratégica e baseada em dados.

### 🎯 Principais Funcionalidades

- **⛏️ Garimpo Automatizado**: Identifica ofertas em alta no ClickBank e Hotmart
- **✍️ Copy IA Avançada**: Otimiza copies usando princípios dos mestres do copywriting
- **📦 Criação de Entregáveis**: Gera e-books, checklists e workbooks automaticamente
- **📊 Analytics Inteligente**: Visualiza dados e tendências de mercado
- **🌍 Suporte Multilíngue**: Cria conteúdo em português, inglês, espanhol e mais

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Descrição |
|------------|------------|-----------|
| **Interface** | Streamlit | Interface web moderna e responsiva |
| **Automação** | Selenium | Web scraping para garimpo de ofertas |
| **Dados** | Pandas | Análise e manipulação de dados |
| **IA** | OpenAI/Gemini | Geração de conteúdo com IA |
| **Framework** | LangChain | Orquestração de modelos de linguagem |

## 🏗️ Arquitetura dos Módulos

### 📊 Módulo 1: Garimpo de Ofertas
Automatiza a pesquisa de mercado para identificar ofertas e produtos de alta performance:
- Extração de dados do ClickBank e Hotmart
- Análise de métricas de performance (gravidade, comissões)
- Identificação de tendências e oportunidades
- Exportação de dados em CSV/Excel

### ✍️ Módulo 2: Modelagem de Copy
Cria e otimiza copies usando princípios dos mestres do copywriting:
- **Alex Hormozi**: Ofertas irresistíveis e escassez
- **Russell Brunson**: Storytelling e funis de vendas
- **Jon Benson**: Video copywriting fluido
- **Dan Kennedy**: Headlines magnéticas
- **Eugene Schwartz**: Níveis de consciência

### 📦 Módulo 3: Criação de Entregáveis
Gera automaticamente produtos digitais de alto valor:
- E-books estruturados com capítulos
- Checklists acionáveis
- Workbooks interativos
- Scripts para VSL
- Sequências de e-mail para nutrição

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos

- Python 3.8 ou superior
- Git
- Chave de API da OpenAI ou Google Gemini

### ⚡ Instalação Rápida

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/marketing-ecosystem.git
   cd marketing-ecosystem
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas chaves de API
   ```

5. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

6. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

## 📁 Estrutura do Projeto

```
marketing_ecosystem/
├── 📄 app.py                    # Interface principal Streamlit
├── 📁 modules/
│   ├── ⛏️ garimpo_module.py     # Garimpo de ofertas
│   ├── ✍️ copy_module.py        # Modelagem de copy
│   └── 📦 entregaveis_module.py # Criação de entregáveis
├── 📁 data/                     # Dados do garimpo (auto-gerado)
├── 📄 requirements.txt          # Dependências Python
├── 📄 .env.example             # Exemplo de configuração
├── 📄 .gitignore               # Arquivos ignorados pelo Git
└── 📄 README.md                # Esta documentação
```

## 🔧 Configuração Avançada

### 🔑 Chaves de API

O sistema suporta dois provedores de IA:

**OpenAI (Recomendado):**
```bash
OPENAI_API_KEY=sk-sua_chave_aqui
```

**Google Gemini (Alternativo):**
```bash
GOOGLE_API_KEY=sua_chave_google_aqui
```

### ⚙️ Configurações do Streamlit

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📖 Como Usar

### 1. 🏠 Página Inicial
- Visão geral do sistema
- Status das configurações
- Guia rápido de uso

### 2. ⛏️ Garimpo de Ofertas
- Clique em "Iniciar Garimpo"
- Aguarde a coleta de dados
- Analise as ofertas em alta
- Exporte os resultados

### 3. ✍️ Modelagem de Copy
- Cole sua copy original
- Configure nicho e público-alvo
- Clique em "Modelar Copy"
- Baixe a versão otimizada

### 4. 📦 Criação de Entregáveis
- Defina o tópico e tipo
- Selecione o idioma
- Gere a estrutura completa
- Use como bônus de valor

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação](#-como-usar)
2. Consulte as [issues existentes](https://github.com/seu-usuario/marketing-ecosystem/issues)
3. Abra uma nova issue se necessário

## 🔮 Roadmap

- [ ] Integração com mais plataformas de afiliação
- [ ] Análise de sentimento em reviews
- [ ] Geração automática de criativos
- [ ] Dashboard de performance
- [ ] API REST para integração
- [ ] Versão mobile

## 👨‍💻 Desenvolvido por

**Manus AI** - Ecossistema de Marketing Inteligente

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐



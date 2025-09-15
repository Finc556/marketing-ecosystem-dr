"""
Interface Principal do Ecossistema de Direct Response

Esta aplicação Streamlit integra todos os módulos do ecossistema:
- Garimpo de Ofertas
- Modelagem de Copy
- Criação de Entregáveis
"""

import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Adicionar o diretório modules ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Importar módulos
try:
    from modules.garimpo_module import iniciar_garimpo
    from modules.copy_module import gerar_copy_modelada
    from modules.entregaveis_module import gerar_entregavel
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="Ecossistema DR - Direct Response",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .module-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar para navegação
st.sidebar.title("🎯 Navegação")
st.sidebar.markdown("---")

# Informações do sistema
st.sidebar.markdown("### 📊 Status do Sistema")
st.sidebar.success("✅ Sistema Online")
st.sidebar.info(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Seleção de módulo
modulo_selecionado = st.sidebar.selectbox(
    "Selecione um Módulo:",
    ("🏠 Início", "⛏️ Garimpo de Ofertas", "✍️ Modelagem de Copy", "📦 Criação de Entregáveis")
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Configurações")

# Seleção do provedor de IA
provider_ia = st.sidebar.selectbox(
    "Provedor de IA:",
    ("openai", "gemini"),
    help="Escolha o provedor de IA para os módulos de copy e entregáveis"
)

# Verificação de API Key
api_key_status = "✅ Configurada" if os.getenv("OPENAI_API_KEY") else "❌ Não configurada"
st.sidebar.markdown(f"**API Key:** {api_key_status}")

# --- PÁGINA INICIAL ---
if modulo_selecionado == "🏠 Início":
    st.markdown('<h1 class="main-header">Ecossistema de Direct Response</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="module-card">
        <h3>🎯 Bem-vindo ao seu Ecossistema Completo de Marketing</h3>
        <p>Esta plataforma unifica a inteligência de mercado e a criação de conteúdo em um único lugar, 
        permitindo que você identifique oportunidades, crie copies de alta conversão e desenvolva 
        entregáveis de valor para suas campanhas de direct response.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas do sistema
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>⛏️</h3>
            <h4>Garimpo</h4>
            <p>Ofertas em Alta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✍️</h3>
            <h4>Copy IA</h4>
            <p>Otimização Avançada</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📦</h3>
            <h4>Entregáveis</h4>
            <p>Bônus de Valor</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Guia rápido
    st.markdown("### 🚀 Guia Rápido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Garimpo de Ofertas**
        - Identifique produtos em alta no ClickBank e Hotmart
        - Analise métricas de performance
        - Encontre oportunidades de afiliação
        """)
        
        st.markdown("""
        **2. Modelagem de Copy**
        - Cole sua copy existente
        - Aplique princípios dos mestres (Hormozi, Brunson, etc.)
        - Gere hooks, corpo otimizado e CTAs
        """)
    
    with col2:
        st.markdown("""
        **3. Criação de Entregáveis**
        - Gere e-books, checklists e workbooks
        - Crie bônus de alto valor
        - Suporte a múltiplos idiomas
        """)

# --- PÁGINA DE GARIMPO DE OFERTAS ---
elif modulo_selecionado == "⛏️ Garimpo de Ofertas":
    st.title("⛏️ Garimpo de Ofertas em Alta")
    st.markdown("Identifique automaticamente as ofertas e produtos que estão performando melhor no mercado.")
    
    # Botão de garimpo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Iniciar Garimpo", type="primary", use_container_width=True):
            with st.spinner('🔍 Garimpando ofertas... Este processo pode levar alguns minutos.'):
                try:
                    resultado = iniciar_garimpo()
                    if resultado.get("sucesso"):
                        st.success(f"✅ Garimpo concluído! {resultado.get('total_ofertas', 0)} ofertas encontradas.")
                        if resultado.get("analise"):
                            st.json(resultado["analise"])
                    else:
                        st.error(f"❌ Erro no garimpo: {resultado.get('erro', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"❌ Erro durante o garimpo: {str(e)}")
    
    st.markdown("---")
    
    # Exibir dados garimpados
    st.subheader("📊 Ofertas Garimpadas")
    
    try:
        # Procurar pelo arquivo mais recente
        data_dir = "data"
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.startswith("ofertas_garimpadas") and f.endswith(".csv")]
            if csv_files:
                # Pegar o arquivo mais recente
                latest_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
                df_ofertas = pd.read_csv(os.path.join(data_dir, latest_file))
                
                # Exibir tabela
                st.dataframe(
                    df_ofertas.head(20),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Ofertas", len(df_ofertas))
                with col2:
                    st.metric("Plataformas", df_ofertas['plataforma'].nunique())
                with col3:
                    if 'categoria' in df_ofertas.columns:
                        st.metric("Categorias", df_ofertas['categoria'].nunique())
                
            else:
                st.info("📝 Nenhum dado de garimpo encontrado. Execute o garimpo para ver os resultados.")
        else:
            st.info("📁 Diretório de dados não encontrado. Execute o garimpo primeiro.")
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")

# --- PÁGINA DE MODELAGEM DE COPY ---
elif modulo_selecionado == "✍️ Modelagem de Copy":
    st.title("✍️ Modelagem e Otimização de Copy")
    st.markdown("Transforme suas copies em máquinas de conversão usando IA treinada com os princípios dos mestres do copywriting.")
    
    # Configurações da copy
    with st.expander("⚙️ Configurações da Modelagem"):
        col1, col2 = st.columns(2)
        with col1:
            nicho_copy = st.text_input("Nicho/Mercado:", placeholder="Ex: emagrecimento, marketing digital, investimentos")
        with col2:
            publico_copy = st.text_input("Público-alvo:", placeholder="Ex: mulheres 25-45 anos, empreendedores iniciantes")
    
    # Área de input da copy
    st.subheader("📝 Sua Copy Original")
    user_copy = st.text_area(
        "Cole sua copy de VSL, anúncio ou e-mail aqui:",
        height=300,
        placeholder="Cole aqui sua copy existente que você quer otimizar..."
    )
    
    # Botão de modelagem
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧠 Modelar Copy", type="primary", use_container_width=True):
            if user_copy.strip():
                with st.spinner('🤖 A IA está analisando e otimizando sua copy...'):
                    try:
                        resultado_copy = gerar_copy_modelada(
                            user_copy, 
                            nicho_copy, 
                            publico_copy, 
                            provider_ia
                        )
                        
                        st.markdown("---")
                        st.subheader("✨ Copy Otimizada")
                        st.markdown(resultado_copy)
                        
                        # Opção de download
                        st.download_button(
                            label="📥 Baixar Copy Otimizada",
                            data=resultado_copy,
                            file_name=f"copy_otimizada_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao processar copy: {str(e)}")
            else:
                st.warning("⚠️ Por favor, insira uma copy para ser modelada.")

# --- PÁGINA DE CRIAÇÃO DE ENTREGÁVEIS ---
elif modulo_selecionado == "📦 Criação de Entregáveis":
    st.title("📦 Criação de Entregáveis e Bônus")
    st.markdown("Gere estruturas completas de produtos digitais de alto valor para usar como bônus ou produtos principais.")
    
    # Configurações do entregável
    col1, col2 = st.columns(2)
    
    with col1:
        topico_entregavel = st.text_input(
            "🎯 Tópico principal:",
            placeholder="Ex: Como criar um negócio online lucrativo"
        )
        
        publico_entregavel = st.text_input(
            "👥 Público-alvo:",
            placeholder="Ex: empreendedores iniciantes"
        )
    
    with col2:
        tipo_entregavel = st.selectbox(
            "📋 Tipo de entregável:",
            ["E-book", "Checklist", "Workbook", "Script de VSL", "Gabarito", "Guia Prático"]
        )
        
        idioma_entregavel = st.selectbox(
            "🌍 Idioma:",
            ["pt", "en", "es", "it", "de", "fr"],
            format_func=lambda x: {
                "pt": "🇧🇷 Português",
                "en": "🇺🇸 Inglês", 
                "es": "🇪🇸 Espanhol",
                "it": "🇮🇹 Italiano",
                "de": "🇩🇪 Alemão",
                "fr": "🇫🇷 Francês"
            }[x]
        )
    
    # Botão de geração
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Gerar Entregável", type="primary", use_container_width=True):
            if topico_entregavel.strip():
                with st.spinner('📝 Criando estrutura do entregável...'):
                    try:
                        resultado_entregavel = gerar_entregavel(
                            topico_entregavel,
                            tipo_entregavel,
                            idioma_entregavel,
                            publico_entregavel,
                            provider_ia
                        )
                        
                        st.markdown("---")
                        st.subheader("📚 Entregável Criado")
                        st.markdown(resultado_entregavel)
                        
                        # Opção de download
                        st.download_button(
                            label="📥 Baixar Estrutura",
                            data=resultado_entregavel,
                            file_name=f"{tipo_entregavel.lower()}_{topico_entregavel[:30].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar entregável: {str(e)}")
            else:
                st.warning("⚠️ Por favor, insira o tópico para gerar o entregável.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🚀 Ecossistema de Direct Response | Desenvolvido com Streamlit e IA
    </div>
    """, 
    unsafe_allow_html=True
)


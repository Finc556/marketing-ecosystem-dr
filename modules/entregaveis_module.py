"""
Módulo 3: Criação de Entregáveis (entregaveis_module.py)

Este módulo utiliza IA para criar estruturas de produtos digitais de alto valor,
como e-books, checklists, workbooks e sequências de e-mail para nutrição de leads.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriadorEntregaveis:
    """
    Classe principal para criação de entregáveis digitais usando IA.
    """
    
    def __init__(self, provider="openai", temperature=0.7):
        """
        Inicializa o criador de entregáveis.
        
        Args:
            provider (str): Provedor de IA ("openai" ou "gemini")
            temperature (float): Temperatura para geração (0.0 a 1.0)
        """
        self.provider = provider
        self.temperature = temperature
        self.llm = None
        self._configurar_llm()
    
    def _configurar_llm(self):
        """
        Configura o modelo de linguagem baseado no provedor escolhido.
        """
        try:
            if self.provider == "openai":
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
                self.llm = OpenAI(api_key=api_key)
                logger.info("OpenAI configurado com sucesso")
                
            elif self.provider == "gemini":
                import google.generativeai as genai
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
                genai.configure(api_key=api_key)
                self.llm = genai.GenerativeModel('gemini-pro')
                logger.info("Google Gemini configurado com sucesso")
                
            else:
                raise ValueError(f"Provedor '{self.provider}' não suportado")
                
        except Exception as e:
            logger.error(f"Erro ao configurar LLM: {e}")
            raise
    
    def _gerar_resposta(self, prompt: str) -> str:
        """
        Gera resposta usando o modelo configurado.
        
        Args:
            prompt (str): Prompt para o modelo
            
        Returns:
            str: Resposta gerada
        """
        try:
            if self.provider == "openai":
                response = self.llm.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif self.provider == "gemini":
                response = self.llm.generate_content(prompt)
                return response.text
                
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            raise
    
    def gerar_entregavel(self, topico: str, tipo: str, idioma: str = "pt", publico_alvo: str = "") -> str:
        """
        Gera a estrutura completa de um entregável digital.
        
        Args:
            topico (str): Tópico principal do entregável
            tipo (str): Tipo de entregável (E-book, Checklist, etc.)
            idioma (str): Idioma do conteúdo
            publico_alvo (str): Descrição do público-alvo
            
        Returns:
            str: Estrutura completa do entregável
        """
        idioma_map = {
            "pt": "Português",
            "en": "Inglês",
            "es": "Espanhol",
            "it": "Italiano",
            "de": "Alemão",
            "fr": "Francês"
        }
        
        idioma_nome = idioma_map.get(idioma, "Português")
        contexto_publico = f"\nPúblico-alvo: {publico_alvo}" if publico_alvo else ""
        
        template = f"""
        Você é um especialista em criação de produtos digitais de alto valor e marketing de resposta direta. 
        Crie um esboço detalhado e estruturado para um {tipo} sobre o tópico "{topico}".
        
        **Especificações:**
        - Idioma: {idioma_nome}
        - Tipo: {tipo}
        - Tópico: {topico}{contexto_publico}
        
        **Diretrizes para criação:**
        
        1. **Valor Imediato:** O conteúdo deve fornecer valor prático e acionável
        2. **Estrutura Lógica:** Organize o conteúdo de forma progressiva e didática
        3. **Aplicabilidade:** Foque em resultados tangíveis e implementáveis
        4. **Engajamento:** Use linguagem envolvente e motivacional
        5. **Completude:** Cubra o tópico de forma abrangente mas focada
        
        **Formato específico por tipo:**
        
        **Se for E-book:**
        - Crie capítulos bem estruturados
        - Inclua introdução, desenvolvimento e conclusão
        - Adicione exercícios práticos e exemplos
        
        **Se for Checklist:**
        - Liste itens acionáveis e específicos
        - Organize por ordem de prioridade ou sequência lógica
        - Inclua critérios de verificação
        
        **Se for Workbook:**
        - Combine teoria com exercícios práticos
        - Inclua espaços para anotações e reflexões
        - Adicione templates e ferramentas
        
        **Se for Script de VSL:**
        - Estruture com hook, problema, solução e CTA
        - Inclua marcações de tempo e pausas
        - Adicione instruções visuais
        
        **Se for Gabarito:**
        - Forneça respostas detalhadas e explicações
        - Inclua critérios de avaliação
        - Adicione dicas de melhoria
        
        ---
        
        Gere a resposta com o seguinte formato:
        
        # 📚 {tipo.upper()}: [TÍTULO ATRATIVO]
        
        ## 🎯 Objetivo
        [Descrição clara do que o usuário vai alcançar]
        
        ## 👥 Para Quem É
        [Perfil do público-alvo ideal]
        
        ## 📋 Estrutura Completa
        
        [Estrutura detalhada com capítulos/seções/itens organizados logicamente]
        
        ## 🚀 Benefícios Principais
        - [Benefício 1]
        - [Benefício 2]
        - [Benefício 3]
        
        ## 💡 Dicas de Implementação
        [Orientações práticas para usar o entregável]
        
        ## 📈 Como Usar Como Bônus
        [Estratégias para posicionar este entregável como bônus de alto valor]
        """
        
        try:
            resposta = self._gerar_resposta(template)
            return resposta
        except Exception as e:
            logger.error(f"Erro ao gerar entregável: {e}")
            return f"Erro ao processar entregável: {str(e)}"

# Função de conveniência para uso externo (compatibilidade com interface)
def gerar_entregavel(topico: str, tipo: str, idioma: str = "pt", publico_alvo: str = "", provider: str = "openai") -> str:
    """
    Função simplificada para gerar entregável.
    """
    try:
        criador = CriadorEntregaveis(provider=provider)
        return criador.gerar_entregavel(topico, tipo, idioma, publico_alvo)
    except Exception as e:
        return f"Erro ao gerar entregável: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    try:
        resultado = gerar_entregavel(
            topico="Como criar um negócio online lucrativo",
            tipo="E-book",
            idioma="pt",
            publico_alvo="empreendedores iniciantes"
        )
        print("Entregável gerado com sucesso!")
        print(resultado)
    except Exception as e:
        print(f"Erro no teste: {e}")


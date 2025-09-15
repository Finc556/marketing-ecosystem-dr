"""
Módulo 2: O Cérebro de Copy (copy_module.py)

Este módulo utiliza IA para criar e otimizar copies de alta conversão,
baseado nos princípios dos mestres do copywriting como Alex Hormozi,
Russell Brunson, Jon Benson e Dan S. Kennedy.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CerebroCopy:
    """
    Classe principal para geração e otimização de copies usando IA.
    """
    
    def __init__(self, provider="openai", temperature=0.7):
        """
        Inicializa o cérebro de copy.
        
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
                
                # Usar API oficial do OpenAI
                self.llm = OpenAI(
                    api_key=api_key,
                    base_url="https://api.openai.com/v1"  # API oficial
                )
                logger.info("OpenAI configurado com sucesso")
                
            elif self.provider == "gemini":
                import google.generativeai as genai
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
                genai.configure(api_key=api_key)
                self.llm = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini configurado com sucesso")
                
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
                    model="gpt-3.5-turbo",  # Modelo mais estável
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
    
    def gerar_copy_modelada(self, copy_original: str, nicho: str = "", publico_alvo: str = "") -> str:
        """
        Modela uma copy existente aplicando princípios dos mestres do copywriting.
        
        Args:
            copy_original (str): Copy original para ser modelada
            nicho (str): Nicho do produto/serviço
            publico_alvo (str): Descrição do público-alvo
            
        Returns:
            str: Copy otimizada formatada
        """
        contexto_adicional = ""
        if nicho:
            contexto_adicional += f"\nNicho: {nicho}"
        if publico_alvo:
            contexto_adicional += f"\nPúblico-alvo: {publico_alvo}"
        
        template = f"""
        Você é um copywriter de elite que modela copies de alta conversão. Seu trabalho é pegar a copy do usuário e otimizá-la com base nos seguintes princípios dos mestres:

        **Alex Hormozi (Ofertas Irresistíveis):**
        - Crie escassez genuína e urgência ética
        - Empilhe valor com bônus estratégicos
        - Use garantias que eliminam o risco
        - Foque no valor percebido vs. preço

        **Russell Brunson (Funis e Storytelling):**
        - Aplique a jornada do herói na narrativa
        - Use histórias que criam conexão emocional
        - Implemente a estrutura Problema-Agitação-Solução
        - Crie curiosidade que mantém a atenção

        **Jon Benson (Video Copywriting):**
        - Torne a copy mais fluida e conversacional
        - Use transições suaves entre seções
        - Aplique o conceito de "edutainment"
        - Mantenha o ritmo envolvente

        **Dan S. Kennedy (Headlines e Persuasão):**
        - Crie headlines magnéticas que param o scroll
        - Use bullets que geram curiosidade intensa
        - Aplique gatilhos psicológicos poderosos
        - Foque em benefícios específicos e tangíveis

        **Eugene Schwartz (Níveis de Consciência):**
        - Identifique o nível de consciência da audiência
        - Adapte a linguagem ao estágio do prospect
        - Use a fórmula AIDA de forma sofisticada

        {contexto_adicional}

        Copy para modelagem:
        {copy_original}

        ---
        Gere a resposta EXATAMENTE com o seguinte formato, sem textos adicionais:

        ## 🎯 HOOKS OTIMIZADOS

        1. **Hook de Curiosidade:** [Hook focado em despertar curiosidade]
        2. **Hook de Benefício:** [Hook focado no principal benefício]
        3. **Hook de Urgência:** [Hook focado em urgência/escassez]
        4. **Hook de Prova Social:** [Hook focado em resultados/depoimentos]
        5. **Hook de Transformação:** [Hook focado na transformação prometida]

        ## 📝 CORPO OTIMIZADO

        [Corpo da copy completamente reescrito e otimizado, aplicando todos os princípios mencionados. Deve ter pelo menos 300 palavras e incluir storytelling, quebra de objeções, empilhamento de valor e transições suaves.]

        ## 🚀 NOVA CHAMADA PARA AÇÃO

        [Chamada para ação poderosa e específica, com urgência e clareza sobre o próximo passo]

        ## 📊 ANÁLISE DA OTIMIZAÇÃO

        **Principais melhorias aplicadas:**
        - [Lista das principais otimizações realizadas]
        - [Princípios específicos utilizados]
        - [Gatilhos psicológicos implementados]
        """
        
        try:
            resposta = self._gerar_resposta(template)
            return resposta
        except Exception as e:
            logger.error(f"Erro ao gerar copy modelada: {e}")
            return f"Erro ao processar copy: {str(e)}"

# Função de conveniência para uso externo (compatibilidade com interface)
def gerar_copy_modelada(copy_original: str, nicho: str = "", publico_alvo: str = "", provider: str = "openai") -> str:
    """
    Função simplificada para gerar copy modelada.
    """
    try:
        cerebro = CerebroCopy(provider=provider)
        return cerebro.gerar_copy_modelada(copy_original, nicho, publico_alvo)
    except Exception as e:
        return f"Erro ao gerar copy: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    copy_teste = "Descubra o segredo para emagrecer 10kg em 30 dias sem dieta restritiva!"
    
    try:
        resultado = gerar_copy_modelada(copy_teste, "emagrecimento", "mulheres 25-45 anos")
        print("Copy modelada gerada com sucesso!")
        print(resultado)
    except Exception as e:
        print(f"Erro no teste: {e}")


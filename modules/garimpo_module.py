"""
Módulo 1: Garimpo de Ofertas (garimpo_module.py)

Este módulo automatiza a pesquisa de mercado para identificar ofertas e produtos 
de alta performance em plataformas como ClickBank, Hotmart e BuyGoods.
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GarimpadorOfertas:
    """
    Classe principal para garimpar ofertas de diferentes plataformas.
    """
    
    def __init__(self, headless=True):
        """
        Inicializa o garimpador com configurações do navegador.
        
        Args:
            headless (bool): Se True, executa o navegador em modo headless
        """
        self.headless = headless
        self.driver = None
        self.dados_ofertas = []
        
        # Criar diretório para dados se não existir
        os.makedirs("data", exist_ok=True)
    
    def _configurar_driver(self):
        """
        Configura e inicializa o driver do Selenium.
        """
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Configurar User-Agent para evitar detecção de bot
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
            
            # Usar webdriver-manager para baixar driver compatível
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            logger.info("Driver configurado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {e}")
            # Fallback: tentar sem webdriver-manager
            try:
                chrome_options = Options()
                if self.headless:
                    chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.implicitly_wait(10)
                logger.info("Driver configurado com fallback")
            except Exception as e2:
                logger.error(f"Erro no fallback: {e2}")
                raise
    
    def _fechar_driver(self):
        """
        Fecha o driver do navegador.
        """
        if self.driver:
            self.driver.quit()
            logger.info("Driver fechado")
    
    def garimpar_clickbank(self):
        """
        Garimpa ofertas do ClickBank Marketplace.
        """
        logger.info("Iniciando garimpo do ClickBank...")
        
        try:
            self.driver.get("https://www.clickbank.com/marketplace/")
            
            # Aguardar carregamento da página
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-list"))
            )
            
            # Extrair dados das ofertas
            ofertas = self.driver.find_elements(By.CSS_SELECTOR, ".results-list .result-row")
            
            for oferta in ofertas[:20]:  # Limitar a 20 ofertas para teste
                try:
                    # Extrair informações da oferta
                    titulo_elem = oferta.find_element(By.CSS_SELECTOR, ".product-title a")
                    titulo = titulo_elem.text.strip()
                    
                    # Gravidade (popularidade)
                    try:
                        gravidade_elem = oferta.find_element(By.CSS_SELECTOR, ".gravity")
                        gravidade = gravidade_elem.text.strip()
                    except NoSuchElementException:
                        gravidade = "N/A"
                    
                    # Comissão inicial
                    try:
                        comissao_elem = oferta.find_element(By.CSS_SELECTOR, ".initial-commission")
                        comissao = comissao_elem.text.strip()
                    except NoSuchElementException:
                        comissao = "N/A"
                    
                    # Categoria
                    try:
                        categoria_elem = oferta.find_element(By.CSS_SELECTOR, ".category")
                        categoria = categoria_elem.text.strip()
                    except NoSuchElementException:
                        categoria = "N/A"
                    
                    # URL da oferta
                    url = titulo_elem.get_attribute("href")
                    
                    oferta_data = {
                        "plataforma": "ClickBank",
                        "titulo": titulo,
                        "gravidade": gravidade,
                        "comissao_inicial": comissao,
                        "categoria": categoria,
                        "url": url,
                        "data_garimpo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    self.dados_ofertas.append(oferta_data)
                    logger.info(f"Oferta extraída: {titulo}")
                    
                except Exception as e:
                    logger.warning(f"Erro ao extrair oferta: {e}")
                    continue
            
            logger.info(f"ClickBank: {len([o for o in self.dados_ofertas if o['plataforma'] == 'ClickBank'])} ofertas extraídas")
            
        except TimeoutException:
            logger.error("Timeout ao carregar página do ClickBank")
        except Exception as e:
            logger.error(f"Erro no garimpo do ClickBank: {e}")
    
    def garimpar_hotmart(self):
        """
        Garimpa ofertas do Hotmart (versão simplificada).
        """
        logger.info("Iniciando garimpo do Hotmart...")
        
        try:
            self.driver.get("https://www.hotmart.com/pt-br/marketplace")
            
            # Aguardar carregamento
            time.sleep(5)
            
            # Tentar encontrar produtos (estrutura pode variar)
            try:
                produtos = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
                
                for produto in produtos[:15]:  # Limitar a 15 produtos
                    try:
                        # Título do produto
                        titulo_elem = produto.find_element(By.CSS_SELECTOR, "h3, .product-title")
                        titulo = titulo_elem.text.strip()
                        
                        # Preço (se disponível)
                        try:
                            preco_elem = produto.find_element(By.CSS_SELECTOR, ".price, .valor")
                            preco = preco_elem.text.strip()
                        except NoSuchElementException:
                            preco = "N/A"
                        
                        # Rating (se disponível)
                        try:
                            rating_elem = produto.find_element(By.CSS_SELECTOR, ".rating, .avaliacao")
                            rating = rating_elem.text.strip()
                        except NoSuchElementException:
                            rating = "N/A"
                        
                        oferta_data = {
                            "plataforma": "Hotmart",
                            "titulo": titulo,
                            "preco": preco,
                            "rating": rating,
                            "gravidade": "N/A",
                            "comissao_inicial": "N/A",
                            "categoria": "Digital",
                            "url": "N/A",
                            "data_garimpo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        self.dados_ofertas.append(oferta_data)
                        logger.info(f"Produto Hotmart extraído: {titulo}")
                        
                    except Exception as e:
                        logger.warning(f"Erro ao extrair produto Hotmart: {e}")
                        continue
                
                logger.info(f"Hotmart: {len([o for o in self.dados_ofertas if o['plataforma'] == 'Hotmart'])} produtos extraídos")
                
            except NoSuchElementException:
                logger.warning("Estrutura da página Hotmart não encontrada")
                
        except Exception as e:
            logger.error(f"Erro no garimpo do Hotmart: {e}")
    
    def analisar_dados(self):
        """
        Analisa os dados coletados e gera insights.
        """
        if not self.dados_ofertas:
            logger.warning("Nenhum dado para analisar")
            return None
        
        df = pd.DataFrame(self.dados_ofertas)
        
        # Análises básicas
        analise = {
            "total_ofertas": len(df),
            "plataformas": df['plataforma'].value_counts().to_dict(),
            "categorias_populares": df['categoria'].value_counts().head(5).to_dict() if 'categoria' in df.columns else {},
        }
        
        # Análise específica do ClickBank (gravidade)
        clickbank_data = df[df['plataforma'] == 'ClickBank']
        if not clickbank_data.empty and 'gravidade' in clickbank_data.columns:
            # Converter gravidade para numérico (remover texto extra)
            clickbank_data = clickbank_data.copy()
            clickbank_data['gravidade_num'] = pd.to_numeric(
                clickbank_data['gravidade'].str.extract('(\d+\.?\d*)')[0], 
                errors='coerce'
            )
            
            if not clickbank_data['gravidade_num'].isna().all():
                analise['clickbank_gravidade_media'] = clickbank_data['gravidade_num'].mean()
                analise['top_gravidade'] = clickbank_data.nlargest(5, 'gravidade_num')[['titulo', 'gravidade']].to_dict('records')
        
        return analise
    
    def salvar_dados(self, formato='csv'):
        """
        Salva os dados coletados em arquivo.
        
        Args:
            formato (str): Formato do arquivo ('csv' ou 'excel')
        """
        if not self.dados_ofertas:
            logger.warning("Nenhum dado para salvar")
            return
        
        df = pd.DataFrame(self.dados_ofertas)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato == 'csv':
            filename = f"data/ofertas_garimpadas_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
        elif formato == 'excel':
            filename = f"data/ofertas_garimpadas_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
        
        logger.info(f"Dados salvos em: {filename}")
        return filename
    
    def iniciar_garimpo_completo(self):
        """
        Executa o garimpo completo em todas as plataformas.
        """
        logger.info("=== INICIANDO GARIMPO COMPLETO ===")
        
        try:
            self._configurar_driver()
            
            # Garimpar cada plataforma
            self.garimpar_clickbank()
            time.sleep(3)  # Pausa entre plataformas
            
            self.garimpar_hotmart()
            
            # Analisar e salvar dados
            analise = self.analisar_dados()
            filename = self.salvar_dados()
            
            logger.info("=== GARIMPO CONCLUÍDO ===")
            
            return {
                "sucesso": True,
                "arquivo_dados": filename,
                "analise": analise,
                "total_ofertas": len(self.dados_ofertas)
            }
            
        except Exception as e:
            logger.error(f"Erro durante garimpo: {e}")
            return {
                "sucesso": False,
                "erro": str(e),
                "total_ofertas": len(self.dados_ofertas)
            }
        
        finally:
            self._fechar_driver()

def iniciar_garimpo(clickbank_user=None, clickbank_pass=None, hotmart_email=None, hotmart_pass=None):
    """
    Função principal para iniciar o processo de garimpo.
    Interface simplificada para uso externo.
    
    Args:
        clickbank_user: Usuário do ClickBank
        clickbank_pass: Senha do ClickBank
        hotmart_email: Email do Hotmart
        hotmart_pass: Senha do Hotmart
    """
    # Configurar credenciais nas variáveis de ambiente temporariamente
    if clickbank_user:
        os.environ['CLICKBANK_USERNAME'] = clickbank_user
    if clickbank_pass:
        os.environ['CLICKBANK_PASSWORD'] = clickbank_pass
    if hotmart_email:
        os.environ['HOTMART_EMAIL'] = hotmart_email
    if hotmart_pass:
        os.environ['HOTMART_PASSWORD'] = hotmart_pass
    
    garimpador = GarimpadorOfertas(headless=True)
    resultado = garimpador.iniciar_garimpo_completo()
    return resultado

# Exemplo de uso
if __name__ == "__main__":
    resultado = iniciar_garimpo()
    print(f"Resultado do garimpo: {resultado}")


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
    
    def garimpar_cbengine(self):
        """
        Garimpa ofertas do CBEngine (dados públicos do ClickBank).
        Extrai dados detalhados da tabela de Top Gravity.
        """
        logger.info("🚀 Iniciando garimpo do CBEngine...")
        
        try:
            # Acessar página de Top Gravity
            self.driver.get("https://cbengine.com/clickbank-top-gravity.html")
            logger.info("📄 Página CBEngine carregada")
            
            # Aguardar carregamento da tabela
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Aguardar um pouco mais para garantir carregamento completo
            time.sleep(3)
            
            ofertas = []
            
            try:
                # Localizar a tabela principal de produtos
                tabela = self.driver.find_element(By.CSS_SELECTOR, "table")
                linhas = tabela.find_elements(By.TAG_NAME, "tr")
                
                logger.info(f"📊 Encontradas {len(linhas)} linhas na tabela")
                
                # Processar cada linha (pular cabeçalho)
                for i, linha in enumerate(linhas[1:21]):  # Top 20 produtos
                    try:
                        colunas = linha.find_elements(By.TAG_NAME, "td")
                        
                        if len(colunas) >= 7:  # Verificar se tem colunas suficientes
                            # Extrair dados de cada coluna
                            rank = str(i + 1)
                            
                            # Coluna 1: Produto (nome e link)
                            produto_cell = colunas[1]
                            produto_links = produto_cell.find_elements(By.TAG_NAME, "a")
                            nome_produto = produto_links[0].text.strip() if produto_links else "N/A"
                            url_produto = produto_links[0].get_attribute("href") if produto_links else "N/A"
                            
                            # Coluna 2: Rank
                            rank_oficial = colunas[0].text.strip() if colunas[0].text.strip() else rank
                            
                            # Coluna 3: Change
                            change = colunas[2].text.strip() if len(colunas) > 2 else "N/A"
                            
                            # Coluna 4: Mntm (Momentum)
                            momentum = colunas[3].text.strip() if len(colunas) > 3 else "N/A"
                            
                            # Coluna 5: Initial $/sale
                            initial_sale = colunas[4].text.strip() if len(colunas) > 4 else "N/A"
                            
                            # Coluna 6: Gravity
                            gravity = colunas[5].text.strip() if len(colunas) > 5 else "N/A"
                            
                            # Coluna 7: Info (ícones de informação)
                            info_cell = colunas[6] if len(colunas) > 6 else None
                            
                            # Extrair categoria do nome do produto (heurística)
                            categoria = self._extrair_categoria_produto(nome_produto)
                            
                            # Criar registro da oferta
                            oferta = {
                                "plataforma": "CBEngine",
                                "titulo": nome_produto,
                                "url": url_produto,
                                "rank_oficial": rank_oficial,
                                "rank_sequencial": rank,
                                "gravidade": gravity,
                                "preco_inicial": initial_sale,
                                "momentum": momentum,
                                "change": change,
                                "categoria": categoria,
                                "comissao_inicial": "50-75%",
                                "fonte_dados": "CBEngine Top Gravity",
                                "data_garimpo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            ofertas.append(oferta)
                            self.dados_ofertas.append(oferta)
                            
                            logger.info(f"✅ #{rank} - {nome_produto} | Gravity: {gravity} | $: {initial_sale}")
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao processar linha {i+1}: {e}")
                        continue
                
                # Tentar coletar dados adicionais de outras páginas
                self._garimpar_cbengine_categorias(ofertas)
                
                logger.info(f"🎯 CBEngine: {len(ofertas)} ofertas coletadas com sucesso")
                
                # Salvar dados específicos do CBEngine
                if ofertas:
                    self._salvar_dados_cbengine(ofertas)
                
                return ofertas
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar tabela CBEngine: {e}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erro durante garimpo CBEngine: {e}")
            return []
    
    def _extrair_categoria_produto(self, nome_produto):
        """
        Extrai categoria do produto baseado no nome (heurística).
        """
        nome_lower = nome_produto.lower()
        
        # Categorias de saúde
        if any(palavra in nome_lower for palavra in ['health', 'weight', 'loss', 'diet', 'fitness', 'muscle', 'supplement', 'nutrition']):
            return "Health & Fitness"
        
        # Categorias de negócios
        elif any(palavra in nome_lower for palavra in ['business', 'money', 'income', 'profit', 'marketing', 'sales', 'entrepreneur']):
            return "Business / Investing"
        
        # Categorias de relacionamento
        elif any(palavra in nome_lower for palavra in ['dating', 'relationship', 'love', 'attraction', 'romance']):
            return "Relationships"
        
        # Categorias de autoajuda
        elif any(palavra in nome_lower for palavra in ['manifestation', 'mindset', 'success', 'motivation', 'self-help', 'personal']):
            return "Self-Help"
        
        # Categorias de tecnologia
        elif any(palavra in nome_lower for palavra in ['software', 'app', 'system', 'tool', 'technology', 'digital']):
            return "Software & Technology"
        
        # Categorias de hobbies
        elif any(palavra in nome_lower for palavra in ['woodworking', 'craft', 'hobby', 'diy', 'art', 'music']):
            return "Hobbies & Crafts"
        
        else:
            return "General"
    
    def _garimpar_cbengine_categorias(self, ofertas_existentes):
        """
        Coleta dados adicionais de categorias específicas do CBEngine.
        """
        try:
            logger.info("📂 Coletando dados de categorias específicas...")
            
            # URLs de categorias populares
            categorias_urls = [
                "https://cbengine.com/clickbank-best-gains.html",  # Best Gains
                "https://cbengine.com/clickbank-new-products.html"  # New Products
            ]
            
            for url in categorias_urls:
                try:
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Processar produtos desta categoria
                    linhas = self.driver.find_elements(By.CSS_SELECTOR, "tr[bgcolor]")
                    
                    for linha in linhas[:5]:  # Top 5 de cada categoria
                        try:
                            colunas = linha.find_elements(By.TAG_NAME, "td")
                            if len(colunas) >= 2:
                                produto_cell = colunas[1]
                                links = produto_cell.find_elements(By.TAG_NAME, "a")
                                nome = links[0].text.strip() if links else "N/A"
                                
                                # Verificar se já não temos este produto
                                if not any(oferta['titulo'] == nome for oferta in ofertas_existentes):
                                    logger.info(f"📝 Produto adicional encontrado: {nome}")
                                    
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar categoria {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao coletar categorias adicionais: {e}")
    
    def _salvar_dados_cbengine(self, ofertas):
        """
        Salva dados específicos do CBEngine em arquivo separado.
        """
        try:
            if ofertas:
                df = pd.DataFrame(ofertas)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo = f"data/cbengine_top_gravity_{timestamp}.csv"
                
                # Criar diretório se não existir
                os.makedirs("data", exist_ok=True)
                
                df.to_csv(arquivo, index=False, encoding='utf-8')
                logger.info(f"💾 Dados CBEngine salvos em: {arquivo}")
                
                # Salvar também em formato JSON para análise
                arquivo_json = f"data/cbengine_top_gravity_{timestamp}.json"
                df.to_json(arquivo_json, orient='records', indent=2)
                logger.info(f"💾 Dados CBEngine salvos em JSON: {arquivo_json}")
                
                return arquivo
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar dados CBEngine: {e}")
            return None
    
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
            
            # Garimpar CBEngine primeiro (não requer login)
            self.garimpar_cbengine()
            time.sleep(3)  # Pausa entre plataformas
            
            # Garimpar ClickBank (requer login)
            self.garimpar_clickbank()
            time.sleep(3)  # Pausa entre plataformas
            
            # Garimpar Hotmart (requer login)
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


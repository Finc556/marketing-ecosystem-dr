# 🔐 Guia de Configuração de Credenciais

## 📋 Visão Geral

Para usar o módulo de garimpo, você precisa fornecer credenciais de acesso às plataformas ClickBank e/ou Hotmart. Este guia explica como obter e configurar essas credenciais.

---

## 🏦 ClickBank

### 📝 Como obter credenciais:

1. **Acesse:** https://www.clickbank.com
2. **Faça login** na sua conta de afiliado
3. **Vá para:** Account Settings > Account Information
4. **Anote:**
   - **Username:** Seu nome de usuário do ClickBank
   - **Password:** Sua senha de login
   - **Account Nickname:** Seu nickname de afiliado (opcional)

### 🔧 Configuração no sistema:

#### Opção 1: Via Interface (Recomendado)
1. Abra o módulo "⛏️ Garimpo de Ofertas"
2. Expanda "🔐 Configurações de Acesso às Plataformas"
3. Preencha os campos do ClickBank
4. Execute o garimpo

#### Opção 2: Via arquivo .env
```bash
CLICKBANK_USERNAME=seu_usuario_clickbank
CLICKBANK_PASSWORD=sua_senha_clickbank
CLICKBANK_ACCOUNT_NICKNAME=seu_nickname_clickbank
```

### 📊 O que o sistema faz:
- Acessa o marketplace do ClickBank
- Extrai dados de ofertas em alta
- Coleta métricas de gravidade e comissão
- Identifica categorias populares

---

## 🔥 Hotmart

### 📝 Como obter credenciais:

#### Para Afiliados:
1. **Acesse:** https://app.hotmart.com
2. **Faça login** na sua conta
3. **Use:**
   - **Email:** Seu email de login
   - **Password:** Sua senha de login

#### Para Produtores (API):
1. **Acesse:** https://developers.hotmart.com
2. **Vá para:** Minhas Aplicações
3. **Crie uma nova aplicação**
4. **Anote:**
   - **Client ID:** ID da aplicação
   - **Client Secret:** Chave secreta

### 🔧 Configuração no sistema:

#### Opção 1: Via Interface (Recomendado)
1. Abra o módulo "⛏️ Garimpo de Ofertas"
2. Expanda "🔐 Configurações de Acesso às Plataformas"
3. Preencha os campos do Hotmart
4. Execute o garimpo

#### Opção 2: Via arquivo .env
```bash
# Para afiliados
HOTMART_EMAIL=seu@email.com
HOTMART_PASSWORD=sua_senha

# Para produtores (API)
HOTMART_CLIENT_ID=seu_client_id
HOTMART_CLIENT_SECRET=seu_client_secret
```

### 📊 O que o sistema faz:
- Acessa o marketplace do Hotmart
- Extrai dados de produtos em alta
- Coleta informações de comissão
- Identifica nichos populares

---

## 🛡️ Segurança das Credenciais

### ✅ Boas Práticas:

1. **Nunca compartilhe** suas credenciais
2. **Use senhas fortes** e únicas
3. **Ative 2FA** quando disponível
4. **Monitore** acessos suspeitos
5. **Revogue** credenciais se necessário

### 🔒 Como o sistema protege:

- **Criptografia:** Credenciais são criptografadas em memória
- **Não armazenamento:** Não salvamos suas credenciais permanentemente
- **Sessões temporárias:** Credenciais são usadas apenas durante o garimpo
- **Logs seguros:** Senhas não aparecem em logs

### ⚠️ Importante:

- O sistema **NÃO salva** suas credenciais no disco
- Você precisa inserir as credenciais a cada uso
- Para conveniência, use o arquivo `.env` (local apenas)

---

## 🚀 Configuração Rápida

### 1. Primeira vez:
```bash
# 1. Clone o repositório
git clone https://github.com/Finc556/marketing-ecosystem-dr.git
cd marketing-ecosystem-dr

# 2. Copie o arquivo de exemplo
cp .env.example .env

# 3. Edite o arquivo .env com suas credenciais
nano .env
```

### 2. Arquivo .env completo:
```bash
# APIs de IA
OPENAI_API_KEY=sk-sua_chave_openai

# ClickBank
CLICKBANK_USERNAME=seu_usuario
CLICKBANK_PASSWORD=sua_senha

# Hotmart
HOTMART_EMAIL=seu@email.com
HOTMART_PASSWORD=sua_senha

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

### 3. Execute:
```bash
streamlit run app.py
```

---

## 🔧 Solução de Problemas

### ❌ "Credenciais inválidas"
**Possíveis causas:**
- Usuário/senha incorretos
- Conta bloqueada ou suspensa
- 2FA ativado (desative temporariamente)
- Captcha na página de login

**Soluções:**
1. Verifique usuário e senha
2. Teste login manual no site
3. Desative 2FA temporariamente
4. Use VPN se necessário

### ❌ "Erro de conexão"
**Possíveis causas:**
- Problema de internet
- Site fora do ar
- Firewall bloqueando

**Soluções:**
1. Verifique sua conexão
2. Teste acesso manual aos sites
3. Configure proxy se necessário

### ❌ "Nenhuma oferta encontrada"
**Possíveis causas:**
- Credenciais incorretas
- Mudança na estrutura do site
- Região bloqueada

**Soluções:**
1. Verifique credenciais
2. Atualize o sistema
3. Use VPN de outro país

---

## 📞 Suporte

### 🆘 Precisa de ajuda?

1. **Verifique este guia** primeiro
2. **Teste login manual** nos sites
3. **Consulte os logs** do sistema
4. **Abra uma issue** no GitHub

### 📧 Contato:

- **GitHub Issues:** https://github.com/Finc556/marketing-ecosystem-dr/issues
- **Documentação:** README.md e MANUAL_DO_USUARIO.md

---

## 🔄 Atualizações

### 📅 Manutenção:

- **Credenciais:** Atualize regularmente
- **Sistema:** Mantenha sempre atualizado
- **Sites:** Podem mudar estrutura

### 🚀 Melhorias futuras:

- [ ] Suporte a mais plataformas
- [ ] Autenticação OAuth
- [ ] Gerenciador de credenciais
- [ ] Rotação automática de sessões

---

**🔐 Suas credenciais estão seguras conosco!**

*Lembre-se: Nunca compartilhe suas credenciais e sempre use senhas fortes.*


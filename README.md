# 🏠 Bot Imobiliário Profissional - Twilio WhatsApp

Sistema profissional de atendimento automatizado para imobiliárias via WhatsApp, usando a API oficial do Twilio.

## ✨ Características

- 🤖 **IA Avançada**: Classificação de intenções e respostas inteligentes
- 🎤 **Suporte a Áudio**: Transcrição automática de mensagens de voz
- 📱 **WhatsApp Oficial**: Usa a API Business do WhatsApp via Twilio
- 🏢 **Customizável**: Fácil adaptação para diferentes imobiliárias
- 📊 **Escalável**: Suporta múltiplas conversas simultâneas
- 🔒 **Seguro**: Sem risco de banimento, totalmente oficial

## 🚀 Início Rápido

### 1. Configuração Inicial

```bash
# Clone ou extraia o projeto
cd bot_imobiliario_twilio

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure as Variáveis

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env e configure:
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - OPENAI_API_KEY
# - Dados da imobiliária (opcional)
```

### 3. Execute o Bot

```bash
python start_bot.py
```

### 4. Configure o Webhook no Twilio

1. O script mostrará a URL do ngrok (ex: https://abc123.ngrok.io)
2. Acesse o console Twilio: [WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
3. Configure em "WHEN A MESSAGE COMES IN":
   - URL: `https://seu-ngrok.ngrok.io/webhook`
   - Method: POST

### 5. Teste!

- Entre no sandbox: envie `join [seu-código]` para o número do Twilio
- Comece a conversar com o bot!

## 💬 Exemplos de Uso

**Busca de Imóveis:**
- "Procuro apartamento para comprar"
- "Quero casa para alugar com 3 quartos"
- "Tem imóvel em Florianópolis?"

**Informações:**
- "Qual o telefone de vocês?"
- "Como funciona o financiamento?"
- "Sobre a empresa"

**Áudio:**
- Envie uma mensagem de voz com qualquer pergunta!

## 🛠️ Customização

### Para Adaptar a Outra Imobiliária:

1. **Edite `data/company_info.json`**:
   - Nome da empresa
   - Informações de contato
   - Sobre a empresa
   - Serviços oferecidos

2. **Atualize `data/properties.json`**:
   - Adicione os imóveis reais
   - Mantenha o formato JSON

3. **Configure `.env`**:
   - COMPANY_NAME
   - COMPANY_PHONE
   - COMPANY_EMAIL

## 📁 Estrutura do Projeto

```
bot_imobiliario_twilio/
├── app.py                  # Aplicação principal Flask
├── handlers/               # Processadores de mensagens
│   ├── message_handler.py  # Processa textos
│   └── audio_handler.py    # Processa áudios
├── services/               # Serviços de negócio
│   ├── ai_service.py       # Integração com OpenAI
│   └── property_service.py # Lógica imobiliária
├── data/                   # Dados customizáveis
│   ├── properties.json     # Lista de imóveis
│   └── company_info.json   # Informações da empresa
└── utils/                  # Utilitários
    └── logger.py           # Sistema de logs
```

## 🚀 Deploy em Produção

### Opção 1: Heroku
```bash
heroku create nome-do-app
heroku config:set TWILIO_ACCOUNT_SID=xxx
heroku config:set TWILIO_AUTH_TOKEN=xxx
heroku config:set OPENAI_API_KEY=xxx
git push heroku main
```

### Opção 2: Railway
```bash
railway login
railway init
railway add
railway up
```

### Opção 3: Servidor Próprio
```bash
# Use gunicorn para produção
gunicorn app:app --bind 0.0.0.0:$PORT
```

## 🔧 Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| TWILIO_ACCOUNT_SID | SID da conta Twilio | ✅ |
| TWILIO_AUTH_TOKEN | Token de autenticação | ✅ |
| OPENAI_API_KEY | Chave da API OpenAI | ✅ |
| COMPANY_NAME | Nome da imobiliária | ❌ |
| COMPANY_PHONE | Telefone da empresa | ❌ |
| COMPANY_EMAIL | Email da empresa | ❌ |
| PORT | Porta do servidor (padrão: 5000) | ❌ |
| LOG_LEVEL | Nível de log (INFO/DEBUG) | ❌ |

## 📊 Monitoramento

- Logs em tempo real no console
- Arquivos de log em `logs/`
- Health check em `/health`
- Status em `/`

## 🤝 Suporte

Para adaptar este bot para sua imobiliária ou adicionar funcionalidades:
- Documentação Twilio: https://www.twilio.com/docs/whatsapp
- Documentação OpenAI: https://platform.openai.com/docs

## 📝 Licença

Este projeto é fornecido como exemplo e pode ser adaptado conforme necessário.

---

**Desenvolvido para revolucionar o atendimento imobiliário!** 🏡

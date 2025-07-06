#!/usr/bin/env python3
"""
Script para configurar o webhook no Twilio
"""

import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def setup_webhook(webhook_url):
    """Configura o webhook no Twilio sandbox"""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("❌ Erro: Configure TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN no arquivo .env")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        # Para sandbox, você precisa configurar manualmente no console
        print(f"""
✅ Para configurar o webhook:

1. Acesse: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Em "Sandbox Configuration", configure:
   
   WHEN A MESSAGE COMES IN:
   {webhook_url}
   Method: POST

3. Clique em "Save"

4. Para testar, envie mensagem para o WhatsApp sandbox!
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_webhook.py <webhook_url>")
        print("Exemplo: python setup_webhook.py https://abc123.ngrok.io/webhook")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    setup_webhook(webhook_url)

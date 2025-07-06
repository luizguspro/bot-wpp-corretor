#!/usr/bin/env python3
"""
Script de inicialização do bot
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def check_requirements():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import flask
        import twilio
        import openai
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError:
        print("❌ Dependências não encontradas.")
        print("📦 Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_env():
    """Verifica configurações do ambiente"""
    load_dotenv()
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Variáveis faltando no .env: {', '.join(missing)}")
        print("📝 Copie .env.example para .env e configure as variáveis")
        return False
    
    print("✅ Configurações do ambiente OK!")
    return True

def start_ngrok():
    """Inicia o ngrok"""
    print("🌐 Iniciando ngrok...")
    print("Se não tiver o ngrok, baixe em: https://ngrok.com/download")
    
    # Verifica se ngrok está instalado
    try:
        subprocess.run(["ngrok", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ngrok não encontrado!")
        print("📥 Baixe em: https://ngrok.com/download")
        return None
    
    # Inicia ngrok em background
    port = os.environ.get('PORT', '5000')
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", port],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"✅ ngrok iniciado na porta {port}")
    print("📱 Use a URL HTTPS do ngrok para configurar o webhook")
    time.sleep(3)
    
    return ngrok_process

def main():
    print("🚀 Iniciando Bot Imobiliário com Twilio...")
    print("=" * 50)
    
    # Verifica requisitos
    if not check_requirements():
        return
    
    if not check_env():
        return
    
    # Pergunta sobre ngrok
    use_ngrok = input("\n🌐 Deseja iniciar o ngrok para testes locais? (s/n): ").lower() == 's'
    
    ngrok_process = None
    if use_ngrok:
        ngrok_process = start_ngrok()
        if ngrok_process:
            print("\n📌 IMPORTANTE:")
            print("1. Abra http://localhost:4040 para ver a URL do ngrok")
            print("2. Configure a URL no Twilio sandbox")
            print("3. A URL será algo como: https://abc123.ngrok.io/webhook")
            input("\nPressione ENTER após configurar o webhook no Twilio...")
    
    # Inicia o bot
    print("\n🤖 Iniciando o bot...")
    os.environ['START_TIME'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        if os.name == 'nt':  # Windows
            subprocess.call([sys.executable, "app.py"])
        else:  # Linux/Mac
            subprocess.call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Bot encerrado!")
    finally:
        if ngrok_process:
            ngrok_process.terminate()

if __name__ == "__main__":
    main()

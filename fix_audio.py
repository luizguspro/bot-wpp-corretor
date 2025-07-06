from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from handlers.message_handler import MessageHandler
from handlers.audio_handler import AudioHandler
from utils.logger import setup_logger

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logger = setup_logger()

# Inicializa Flask
app = Flask(__name__)

# Inicializa handlers
message_handler = MessageHandler()
audio_handler = AudioHandler()

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """Webhook principal que recebe mensagens do WhatsApp via Twilio"""
    try:
        # DEBUG: Log completo da requisição
        logger.info("="*50)
        logger.info("🔍 NOVA MENSAGEM RECEBIDA")
        logger.info(f"🔍 DEBUG - Form data completo: {dict(request.form)}")
        logger.info(f"🔍 DEBUG - NumMedia: {request.values.get('NumMedia', '0')}")
        logger.info(f"🔍 DEBUG - MediaUrl0: {request.values.get('MediaUrl0', 'None')}")
        logger.info(f"🔍 DEBUG - MediaContentType0: {request.values.get('MediaContentType0', 'None')}")
        logger.info("="*50)
        
        # Extrai dados da requisição
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        # Verifica se há mídia
        num_media = int(request.values.get('NumMedia', 0))
        
        logger.info(f"📨 Mensagem recebida de {from_number}")
        logger.info(f"💬 Texto do corpo: '{incoming_msg}'")
        logger.info(f"📎 Número de mídias: {num_media}")
        
        # Cria resposta Twilio
        resp = MessagingResponse()
        msg = resp.message()
        
        # Processa mídia se houver
        if num_media > 0:
            media_url = request.values.get('MediaUrl0', '')
            media_type = request.values.get('MediaContentType0', '')
            
            logger.info(f"🎭 Tipo de mídia detectado: {media_type}")
            logger.info(f"🔗 URL da mídia: {media_url[:50]}...")
            
            # WhatsApp pode enviar áudio como vários tipos
            audio_types = ['audio/', 'application/ogg', 'video/mp4', 'audio/ogg', 'audio/mpeg']
            is_audio = any(audio_type in media_type.lower() for audio_type in audio_types)
            
            logger.info(f"🎵 É áudio? {is_audio}")
            
            if is_audio:
                logger.info(f"🎤 ÁUDIO DETECTADO! Tipo: {media_type}")
                logger.info(f"🎤 Iniciando processamento de áudio...")
                response_text = audio_handler.process_audio(media_url, from_number)
            else:
                logger.info(f"📷 Mídia não é áudio. Tipo: {media_type}")
                response_text = f"Recebi sua mídia ({media_type}), mas só consigo processar mensagens de texto e áudio no momento."
        # Processa texto
        elif incoming_msg:
            logger.info(f"💬 Processando texto: {incoming_msg[:50]}...")
            response_text = message_handler.process_message(incoming_msg, from_number)
        else:
            logger.info("❓ Mensagem vazia recebida")
            response_text = "Desculpe, não consegui processar sua mensagem. Por favor, envie um texto ou áudio."
        
        # Envia resposta
        msg.body(response_text)
        logger.info(f"✅ Resposta sendo enviada: {response_text[:100]}...")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"❌ ERRO NO WEBHOOK: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.")
        return str(resp)

@app.route("/", methods=["GET"])
def home():
    """Endpoint de verificação"""
    return jsonify({
        "status": "online",
        "service": "Bot Imobiliário - Twilio WhatsApp",
        "version": "2.0",
        "debug": "enabled"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": os.environ.get('START_TIME', 'unknown')
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Bot iniciado na porta {port}")
    logger.info(f"🔍 Modo DEBUG ativado - Logs detalhados habilitados")
    app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from handlers.message_handler import MessageHandler
from handlers.audio_handler import AudioHandler
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger()

app = Flask(__name__)
message_handler = MessageHandler()
audio_handler = AudioHandler()

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        num_media = int(request.values.get('NumMedia', 0))
        
        logger.info(f"Mensagem de {from_number}: {incoming_msg[:50]}...")
        
        resp = MessagingResponse()
        
        if num_media > 0:
            media_url = request.values.get('MediaUrl0', '')
            media_type = request.values.get('MediaContentType0', '')
            
            if 'audio' in media_type.lower():
                result = audio_handler.process_audio(media_url, from_number)
                response_text = result if isinstance(result, str) else result.get('text', '')
                msg = resp.message(response_text)
            else:
                # Usa emoji unicode
                msg = resp.message("Recebi sua mídia! Me conta o que você procura! \U0001F3E0")
        else:
            result = message_handler.process_message(incoming_msg, from_number)
            
            if isinstance(result, dict):
                response_text = result.get('text', '')
                media_urls = result.get('media', [])
                
                msg = resp.message(response_text)
                
                for media_url in media_urls[:3]:
                    msg.media(media_url)
            else:
                msg = resp.message(result)
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        # Emoji unicode
        msg = resp.message("Ops! Tive um probleminha aqui... \U0001F605 Digite 'oi' para recomeçar!")
        return str(resp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Tony - Bot Imobiliário Inteligente",
        "version": "4.0",
        "personality": "friendly"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Tony Bot iniciado na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=False)

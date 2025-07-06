import logging
import requests
import tempfile
import os
from services.ai_service import AIService
from handlers.message_handler import MessageHandler

logger = logging.getLogger(__name__)

class AudioHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.message_handler = MessageHandler()
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    def process_audio(self, media_url: str, from_number: str) -> str:
        """Processa mensagens de áudio"""
        temp_file_path = None
        try:
            logger.info(f"🎵 Processando áudio de {from_number}")
            logger.info(f"📎 URL da mídia: {media_url}")
            
            # Baixa o áudio da Twilio
            logger.info("⬇️ Baixando áudio...")
            response = requests.get(
                media_url,
                auth=(self.account_sid, self.auth_token),
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            # Salva temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
                file_size = temp_file.tell()
            
            logger.info(f"✅ Áudio salvo: {file_size} bytes")
            
            # Transcreve usando OpenAI Whisper
            logger.info("🎯 Iniciando transcrição com Whisper...")
            transcribed_text = self.ai_service.transcribe_audio(temp_file_path)
            
            if not transcribed_text:
                logger.error("❌ Transcrição retornou vazia")
                return "Desculpe, não consegui entender o áudio. Por favor, tente enviar uma mensagem de texto."
            
            logger.info(f"📝 Transcrição concluída: {transcribed_text[:100]}...")
            
            # Processa o texto transcrito
            return self.message_handler.process_message(transcribed_text, from_number)
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar áudio: {str(e)}", exc_info=True)
            return "Desculpe, ocorreu um erro ao processar seu áudio. Por favor, tente enviar uma mensagem de texto."
        
        finally:
            # Remove arquivo temporário
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info("🗑️ Arquivo temporário removido")
                except:
                    pass
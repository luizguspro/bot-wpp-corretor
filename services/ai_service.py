import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"
        else:
            self.client = None
            logger.warning("OpenAI API key não configurada - usando respostas padrão")
    
    def generate_contextual_response(self, text, context):
        """Gera resposta com contexto da conversa"""
        if not self.client:
            return self._fallback_response(text)
        
        try:
            system_prompt = f"""Você é o Tony, um corretor de imóveis carismático e prestativo.
            
Contexto da conversa:
- Nome do cliente: {context.get('name', 'não informado')}
- Preferências: {context.get('preferences', {})}
- Última busca: {context.get('last_search', 'nenhuma')}

Seja entusiasmado, útil e sempre sugira próximos passos.
Use emojis com moderação.
Máximo 3 frases."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro AI: {e}")
            return self._fallback_response(text)
    
    def _fallback_response(self, text):
        """Resposta quando AI não está disponível"""
        text_lower = text.lower()
        
        if 'obrigado' in text_lower or 'obrigada' in text_lower:
            return "Por nada! Foi um prazer ajudar! Qualquer coisa é só chamar! 😊"
        elif 'tchau' in text_lower or 'até' in text_lower:
            return "Até logo! Foi ótimo conversar com você! Volte sempre! 👋"
        elif '?' in text:
            return "Ótima pergunta! Me conta mais detalhes para eu poder ajudar melhor!"
        elif any(word in text_lower for word in ['sim', 'quero', 'gostei']):
            return "Que legal! Vamos em frente então! Como posso ajudar?"
        elif any(word in text_lower for word in ['não', 'nao']):
            return "Sem problemas! Que tal tentarmos outra opção?"
        else:
            return "Entendi! Como posso ajudar você com isso?"
    
    def generate_response(self, text):
        """Método de compatibilidade"""
        return self.generate_contextual_response(text, {})
    
    def transcribe_audio(self, audio_path):
        """Transcreve áudio usando Whisper"""
        if not self.client:
            return ""
        
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"
                )
            return transcript.text
        except Exception as e:
            logger.error(f"Erro transcrição: {e}")
            return ""

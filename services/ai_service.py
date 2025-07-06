import os
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def classify_intent(self, text: str) -> dict:
        """Classifica a intenção da mensagem"""
        try:
            # Detecção rápida de intenções comuns
            text_lower = text.lower()
            
            # Como vocês podem ajudar = info sobre a empresa
            if any(phrase in text_lower for phrase in ['como vocês', 'como vcs', 'o que fazem', 'quais serviços']):
                return {"intent": "company_info", "parameters": {"info_type": "about"}}
            
            # Busca de imóveis
            if any(word in text_lower for word in ['procuro', 'quero', 'preciso', 'busco']):
                params = {}
                if 'apartamento' in text_lower:
                    params['tipo'] = 'apartamento'
                elif 'casa' in text_lower:
                    params['tipo'] = 'casa'
                
                if 'comprar' in text_lower or 'venda' in text_lower:
                    params['operacao'] = 'venda'
                elif 'alugar' in text_lower or 'aluguel' in text_lower:
                    params['operacao'] = 'aluguel'
                
                # Extrai número de quartos
                import re
                quartos_match = re.search(r'(\d+)\s*quarto', text_lower)
                if quartos_match:
                    params['quartos'] = int(quartos_match.group(1))
                
                return {"intent": "property_search", "parameters": params}
            
            # Fotos
            if any(word in text_lower for word in ['foto', 'imagem', 'ver', 'mostra']):
                return {"intent": "show_photos", "parameters": {}}
            
            # Contato
            if any(word in text_lower for word in ['contato', 'telefone', 'endereço', 'horário']):
                return {"intent": "company_info", "parameters": {"info_type": "contato"}}
            
            # Financiamento
            if 'financiamento' in text_lower:
                return {"intent": "company_info", "parameters": {"info_type": "financiamento"}}
            
            # Script de vendas
            if 'script' in text_lower and any(word in text_lower for word in ['venda', 'corretor']):
                return {"intent": "sales_script", "parameters": {}}
            
            # Caso geral - usa GPT para classificar
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Classifique a intenção em:
                        - property_search: busca por imóveis
                        - company_info: informações sobre a empresa
                        - sales_script: ajuda com vendas
                        - general: outros assuntos
                        
                        Retorne JSON: {"intent": "categoria", "parameters": {}}"""
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Erro na classificação: {str(e)}")
            return {"intent": "general", "parameters": {}}
    
    def generate_response(self, text: str) -> str:
        """Gera resposta usando IA para casos gerais"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um assistente virtual de uma imobiliária.
                        Seja sempre educado, profissional e prestativo.
                        Responda de forma concisa e clara.
                        Sempre termine oferecendo ajuda para encontrar imóveis."""
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return "Como posso ajudar você a encontrar o imóvel ideal?"
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcreve áudio usando Whisper"""
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"
                )
            
            return transcript.text
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {str(e)}")
            return ""

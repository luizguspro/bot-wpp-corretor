import os
import json
import logging
from openai import OpenAI
from services.sentiment_analyzer import SentimentAnalyzer
from services.language_detector import LanguageDetector
from services.demo_mode import DemoMode

logger = logging.getLogger(__name__)

class AIPremiumService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.sentiment = SentimentAnalyzer()
        self.language = LanguageDetector()
        self.demo = DemoMode()
        self.model = "gpt-4o-mini"
    
    def process_with_sentiment(self, text: str) -> dict:
        """Processa mensagem com análise completa"""
        # Detecta idioma
        language = self.language.detect_language(text)
        
        # Analisa sentimento
        sentiment_data = self.sentiment.analyze(text)
        
        # Ativa modo demo se solicitado
        if "modo demo" in text.lower():
            return {
                "response": self.demo.activate(),
                "sentiment": "positive",
                "language": language
            }
        
        # Classifica intenção
        intent_data = self.classify_intent(text)
        
        # Gera resposta apropriada
        tone_prompts = {
            "empathetic_urgent": "Seja extremamente empático e priorize resolver rapidamente.",
            "helpful_urgent": "Seja muito prestativo e ágil na resposta.",
            "friendly_enthusiastic": "Seja caloroso, entusiasmado e positivo.",
            "empathetic_helpful": "Seja compreensivo e ofereça soluções práticas.",
            "professional_friendly": "Seja profissional mas acessível."
        }
        
        system_prompt = f"""Você é um assistente imobiliário especializado.
        Idioma detectado: {language}
        Tom de resposta: {tone_prompts.get(sentiment_data['tone'], 'professional_friendly')}
        Sentimento do cliente: {sentiment_data['sentiment']} {sentiment_data['emoji']}
        {'URGENTE! Priorize esta resposta.' if sentiment_data['urgency'] else ''}
        
        Responda SEMPRE no idioma {language}."""
        
        response = self.generate_contextual_response(text, system_prompt)
        
        # Aplica melhorias do modo demo
        if self.demo.active:
            response = self.demo.get_enhanced_response(response)
        
        return {
            "response": response,
            "sentiment": sentiment_data,
            "language": language,
            "intent": intent_data
        }
    
    def classify_intent(self, text: str) -> dict:
        """Classificação melhorada de intenção"""
        # Similar ao original mas com mais categorias
        pass
    
    def generate_contextual_response(self, text: str, system_prompt: str) -> str:
        """Gera resposta contextualizada"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, houve um erro. Por favor, tente novamente."

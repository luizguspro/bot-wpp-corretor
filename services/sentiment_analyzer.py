from typing import Dict, Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.urgent_keywords = [
            "urgente", "urgência", "rápido", "hoje", "agora", 
            "imediato", "já", "preciso muito", "desesperado"
        ]
        self.positive_keywords = [
            "ótimo", "excelente", "perfeito", "maravilhoso", 
            "adorei", "incrível", "obrigado", "agradeço"
        ]
        self.negative_keywords = [
            "ruim", "péssimo", "horrível", "não gostei", 
            "insatisfeito", "problema", "reclamação", "difícil"
        ]
    
    def analyze(self, text: str) -> Dict:
        """Analisa o sentimento e urgência da mensagem"""
        text_lower = text.lower()
        
        # Detecta urgência
        urgency_score = sum(1 for word in self.urgent_keywords if word in text_lower)
        is_urgent = urgency_score > 0
        
        # Detecta sentimento
        positive_score = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_score = sum(1 for word in self.negative_keywords if word in text_lower)
        
        if positive_score > negative_score:
            sentiment = "positive"
            emoji = "😊"
        elif negative_score > positive_score:
            sentiment = "negative"
            emoji = "😔"
        else:
            sentiment = "neutral"
            emoji = "🤔"
        
        return {
            "sentiment": sentiment,
            "urgency": is_urgent,
            "urgency_level": min(urgency_score * 33, 100),  # 0-100%
            "emoji": emoji,
            "tone": self._get_response_tone(sentiment, is_urgent)
        }
    
    def _get_response_tone(self, sentiment: str, is_urgent: bool) -> str:
        """Determina o tom da resposta baseado na análise"""
        if is_urgent and sentiment == "negative":
            return "empathetic_urgent"  # Máxima prioridade
        elif is_urgent:
            return "helpful_urgent"
        elif sentiment == "positive":
            return "friendly_enthusiastic"
        elif sentiment == "negative":
            return "empathetic_helpful"
        else:
            return "professional_friendly"

from typing import Dict

class LanguageDetector:
    def __init__(self):
        self.language_patterns = {
            "en": ["hello", "house", "apartment", "rent", "buy", "how much", "where", "when"],
            "es": ["hola", "casa", "apartamento", "alquiler", "comprar", "cuánto", "dónde", "cuándo"],
            "pt": ["olá", "oi", "casa", "apartamento", "alugar", "comprar", "quanto", "onde", "quando"]
        }
        
        self.greetings = {
            "pt": "Olá! Como posso ajudar você hoje? 🏠",
            "en": "Hello! How can I help you today? 🏠",
            "es": "¡Hola! ¿Cómo puedo ayudarte hoy? 🏠"
        }
        
        self.responses = {
            "property_found": {
                "pt": "Encontrei {} imóveis perfeitos para você!",
                "en": "I found {} perfect properties for you!",
                "es": "¡Encontré {} propiedades perfectas para ti!"
            },
            "no_results": {
                "pt": "Não encontrei imóveis com essas características.",
                "en": "I couldn't find properties with those characteristics.",
                "es": "No encontré propiedades con esas características."
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detecta o idioma da mensagem"""
        text_lower = text.lower()
        scores = {}
        
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for word in patterns if word in text_lower)
            scores[lang] = score
        
        # Se não detectar, assume português
        detected = max(scores, key=scores.get) if max(scores.values()) > 0 else "pt"
        return detected
    
    def get_response(self, key: str, language: str, *args) -> str:
        """Retorna resposta no idioma correto"""
        template = self.responses.get(key, {}).get(language, self.responses[key]["pt"])
        return template.format(*args) if args else template

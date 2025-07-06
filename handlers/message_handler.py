import logging
from services.ai_service import AIService
from services.property_service import PropertyService

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.property_service = PropertyService()
    
    def process_message(self, text: str, from_number: str) -> str:
        """Processa mensagens de texto"""
        try:
            # Primeiro verifica se é pedido de fotos
            photo_keywords = ['foto', 'fotos', 'imagem', 'imagens', 'ver', 'mostra', 'tour', 'virtual']
            property_codes = ['AP001', 'AP002', 'AP003', 'AP004', 'CA001', 'CA002', 'CA003', 'CA004', 'CA005']
            
            text_upper = text.upper()
            is_photo_request = any(keyword in text.lower() for keyword in photo_keywords)
            has_property_code = any(code in text_upper for code in property_codes)
            
            # Se tem pedido de foto E código de imóvel
            if is_photo_request and has_property_code:
                photo_response = self.property_service.get_property_photos(text)
                if photo_response:
                    return photo_response
            
            # Se só tem pedido de foto genérico
            elif is_photo_request and 'tour' in text.lower():
                return """🎥 *Tours Virtuais Disponíveis*

Vários de nossos imóveis possuem tour virtual 360°!

Para ver o tour virtual, me informe o código do imóvel.
Exemplo: "Quero ver o tour virtual do AP001"

Ou me diga que tipo de imóvel procura e mostro as opções com tour disponível!"""
            
            # Caso contrário, processa normalmente
            intent_data = self.ai_service.classify_intent(text)
            logger.info(f"📊 Intenção classificada: {intent_data.get('intent', 'unknown')}")
            
            # Gera resposta baseada na intenção
            response = self._generate_response(intent_data, text)
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return "Desculpe, não consegui processar sua mensagem. Por favor, tente novamente."
    
    def _generate_response(self, intent_data: dict, original_text: str) -> str:
        """Gera resposta baseada na intenção"""
        intent = intent_data.get('intent', 'general')
        params = intent_data.get('parameters', {})
        
        if intent == 'property_search':
            return self.property_service.search_properties(params)
        
        elif intent == 'company_info':
            return self.property_service.get_company_info(params.get('info_type'))
        
        elif intent == 'sales_script':
            return self.property_service.get_sales_script()
        
        else:
            # Usa IA para resposta geral
            return self.ai_service.generate_response(original_text)

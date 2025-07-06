import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        self.properties = self._load_properties()
    
    def _load_properties(self):
        """Carrega propriedades com imagens"""
        try:
            import json
            with open('data/properties.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def get_property_images(self, property_code: str) -> Dict:
        """Retorna imagens de um imóvel específico"""
        for prop in self.properties:
            if prop.get('codigo', '').upper() == property_code.upper():
                return {
                    "found": True,
                    "images": prop.get('imagens', []),
                    "tour_virtual": prop.get('tour_virtual', None),
                    "property": prop
                }
        
        return {"found": False, "images": [], "tour_virtual": None}
    
    def format_image_response(self, property_code: str) -> str:
        """Formata resposta com imagens"""
        result = self.get_property_images(property_code)
        
        if not result['found']:
            return f"Desculpe, não encontrei o imóvel com código {property_code}."
        
        prop = result['property']
        images = result['images']
        tour = result['tour_virtual']
        
        response = f"🏠 *{prop['tipo']} - {prop['codigo']}*\n"
        response += f"📍 {prop['bairro']}, {prop['cidade']}\n\n"
        
        if images:
            response += f"📸 *{len(images)} fotos disponíveis:*\n"
            for i, img_url in enumerate(images[:3], 1):  # Limita a 3 imagens
                response += f"Foto {i}: {img_url}\n"
        
        if tour:
            response += f"\n🎥 *Tour Virtual 360°:*\n{tour}\n"
        
        response += f"\n💰 Valor: R$ {prop['preco']}\n"
        response += "\n📱 Gostaria de agendar uma visita?"
        
        return response
    
    def has_image_request(self, text: str) -> bool:
        """Detecta se o usuário quer ver imagens"""
        image_keywords = ['foto', 'fotos', 'imagem', 'imagens', 'ver', 'mostra', 'manda', 'tour', 'vídeo', '360']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in image_keywords)

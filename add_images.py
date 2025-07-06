#!/usr/bin/env python3
"""
Script para adicionar suporte a imagens no bot
Execute: python add_images.py
"""

import json
import os

def add_image_support():
    print("🖼️ Adicionando suporte a imagens...")
    
    # 1. Atualizar dados dos imóveis com URLs de imagens
    properties_with_images = [
        {
            "codigo": "AP001",
            "tipo": "Apartamento",
            "operacao": "venda",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "quartos": 3,
            "suites": 1,
            "preco": "750.000,00",
            "descricao": "Apartamento com vista para o mar, 3 quartos sendo 1 suíte, 2 vagas de garagem.",
            "imagens": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80",
                "https://images.unsplash.com/photo-1560440021-33f9630071b4?w=800&q=80",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80"
            ],
            "tour_virtual": "https://my.matterport.com/show/?m=SxQL3iGyvQk"
        },
        {
            "codigo": "CA002",
            "tipo": "Casa",
            "operacao": "venda",
            "bairro": "Jurerê",
            "cidade": "Florianópolis",
            "quartos": 4,
            "suites": 3,
            "preco": "2.500.000,00",
            "descricao": "Casa em condomínio fechado, 4 suítes, piscina, churrasqueira, 4 vagas.",
            "imagens": [
                "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800&q=80",
                "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800&q=80",
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80"
            ],
            "tour_virtual": "https://my.matterport.com/show/?m=YpnCNX9ZTHm"
        },
        {
            "codigo": "AP003",
            "tipo": "Apartamento",
            "operacao": "aluguel",
            "bairro": "Trindade",
            "cidade": "Florianópolis",
            "quartos": 2,
            "suites": 0,
            "preco": "2.800,00",
            "descricao": "Apartamento próximo à UFSC, 2 quartos, mobiliado, com vaga de garagem.",
            "imagens": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80",
                "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800&q=80",
                "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&q=80"
            ]
        },
        {
            "codigo": "AP004",
            "tipo": "Apartamento",
            "operacao": "venda",
            "bairro": "Agronômica",
            "cidade": "Florianópolis",
            "quartos": 2,
            "suites": 1,
            "preco": "580.000,00",
            "descricao": "Apartamento novo, 2 quartos sendo 1 suíte, sacada com churrasqueira.",
            "imagens": [
                "https://images.unsplash.com/photo-1565182999561-18d7dc61c393?w=800&q=80",
                "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=80"
            ]
        },
        {
            "codigo": "CA005",
            "tipo": "Casa",
            "operacao": "aluguel",
            "bairro": "Campeche",
            "cidade": "Florianópolis",
            "quartos": 3,
            "suites": 2,
            "preco": "4.500,00",
            "descricao": "Casa a 200m da praia, 3 quartos sendo 2 suítes, quintal amplo.",
            "imagens": [
                "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=800&q=80",
                "https://images.unsplash.com/photo-1416331108676-a22ccb276e35?w=800&q=80"
            ]
        }
    ]
    
    # Salvar arquivo atualizado
    with open('data/properties.json', 'w', encoding='utf-8') as f:
        json.dump(properties_with_images, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo properties.json atualizado com imagens!")
    
    # 2. Criar serviço de imagens
    image_service = '''import logging
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
        
        response = f"🏠 *{prop['tipo']} - {prop['codigo']}*\\n"
        response += f"📍 {prop['bairro']}, {prop['cidade']}\\n\\n"
        
        if images:
            response += f"📸 *{len(images)} fotos disponíveis:*\\n"
            for i, img_url in enumerate(images[:3], 1):  # Limita a 3 imagens
                response += f"Foto {i}: {img_url}\\n"
        
        if tour:
            response += f"\\n🎥 *Tour Virtual 360°:*\\n{tour}\\n"
        
        response += f"\\n💰 Valor: R$ {prop['preco']}\\n"
        response += "\\n📱 Gostaria de agendar uma visita?"
        
        return response
    
    def has_image_request(self, text: str) -> bool:
        """Detecta se o usuário quer ver imagens"""
        image_keywords = ['foto', 'fotos', 'imagem', 'imagens', 'ver', 'mostra', 'manda', 'tour', 'vídeo', '360']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in image_keywords)
'''
    
    # 3. Atualizar message_handler para detectar pedidos de imagem
    handler_update = '''
    # Adicione este método ao MessageHandler:
    
    def _check_image_request(self, text: str) -> str:
        """Verifica se é um pedido de imagens"""
        # Detecta códigos de imóveis
        import re
        pattern = r'\\b(AP|CA)\\d{3,4}\\b'
        matches = re.findall(pattern, text.upper())
        
        if matches and self.image_service.has_image_request(text):
            return self.image_service.format_image_response(matches[0])
        
        return None
'''

    # 4. Webhook atualizado para enviar imagens via Twilio
    webhook_image_support = '''
# No webhook, adicione suporte para enviar múltiplas mídias:

if "tem fotos" in incoming_msg.lower() or "ver imagens" in incoming_msg.lower():
    # Detecta código do imóvel
    import re
    pattern = r'\\b(AP|CA)\\d{3,4}\\b'
    matches = re.findall(pattern, incoming_msg.upper())
    
    if matches:
        property_code = matches[0]
        image_data = image_service.get_property_images(property_code)
        
        if image_data['found'] and image_data['images']:
            # Envia texto primeiro
            msg.body(f"📸 Aqui estão as fotos do {property_code}:")
            
            # Envia cada imagem
            for img_url in image_data['images'][:3]:  # Máximo 3 imagens
                msg.media(img_url)
            
            # Adiciona tour virtual se houver
            if image_data['tour_virtual']:
                resp.message(f"🎥 Tour Virtual 360°: {image_data['tour_virtual']}")
'''

    # Criar arquivos
    files = {
        "services/image_service.py": image_service,
        "docs/image_handler_update.txt": handler_update,
        "docs/webhook_image_update.txt": webhook_image_support
    }
    
    for filepath, content in files.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Criado: {filepath}")
    
    print("\n📸 SUPORTE A IMAGENS ADICIONADO!")
    print("\n🎯 Perguntas para testar:")
    print('- "Tem fotos do AP001?"')
    print('- "Me mostra imagens da casa CA002"')
    print('- "Quero ver o apartamento AP003 com fotos"')
    print('- "Tem tour virtual?"')
    print("\n💡 Nota: O Twilio suporta envio de imagens!")
    print("As URLs das imagens serão enviadas como links clicáveis.")

if __name__ == "__main__":
    add_image_support()
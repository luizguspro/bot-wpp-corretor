#!/usr/bin/env python3
"""
Correção da detecção de códigos de imóveis
"""

# Abra o arquivo services/property_service.py e encontre o método get_property_photos
# Substitua TODO o método por este código corrigido:

def get_property_photos(self, text: str) -> str:
    """Retorna fotos de um imóvel específico"""
    import re
    
    # Regex corrigido para capturar o código completo
    pattern = r'\b(AP|CA)\d{3,4}\b'
    matches = re.findall(pattern, text.upper())
    
    if not matches:
        # Tenta encontrar menções a códigos específicos
        for prop in self.properties:
            codigo = prop.get('codigo', '')
            if codigo and codigo in text.upper():
                matches = [codigo]
                break
    
    if not matches:
        return None
    
    property_code = matches[0]
    
    # Debug
    print(f"DEBUG: Procurando fotos para código: {property_code}")
    
    # Busca o imóvel
    for prop in self.properties:
        if prop.get('codigo', '') == property_code:
            response = f"📸 *{prop['tipo']} - {prop['codigo']}*\n"
            response += f"📍 {prop.get('bairro', '')}, {prop.get('cidade', '')}\n\n"
            
            # Adiciona fotos se existirem
            fotos = prop.get('fotos', [])
            if fotos:
                response += f"🖼️ *{len(fotos)} fotos disponíveis:*\n\n"
                for i, foto_url in enumerate(fotos, 1):
                    response += f"📷 Foto {i}: {foto_url}\n"
            else:
                response += "Desculpe, ainda não temos fotos deste imóvel disponíveis.\n"
            
            # Adiciona tour virtual se existir
            tour = prop.get('tour_virtual')
            if tour:
                response += f"\n🎥 *Tour Virtual 360°:*\n{tour}\n"
            
            response += f"\n💰 Valor: R$ {prop.get('preco', 'Consulte')}\n"
            response += "\n📱 Interessado? Posso agendar uma visita!"
            
            return response
    
    return f"Desculpe, não encontrei o imóvel {property_code} em nosso sistema."
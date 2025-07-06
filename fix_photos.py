#!/usr/bin/env python3
"""
Correção rápida para adicionar suporte a fotos
Execute: python fix_photos.py
"""

import json

def fix_photo_support():
    print("🖼️ Adicionando suporte rápido a fotos...")
    
    # 1. Atualizar o arquivo de propriedades com imagens
    properties_with_photos = [
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
            "fotos": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"
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
            "fotos": [
                "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800",
                "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800"
            ]
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
            "fotos": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"
            ]
        }
    ]
    
    # Salvar no arquivo correto
    with open('data/properties.json', 'w', encoding='utf-8') as f:
        json.dump(properties_with_photos, f, ensure_ascii=False, indent=2)
    print("✅ Arquivo properties.json atualizado com fotos!")
    
    # 2. Atualizar o property_service.py
    property_service_update = '''import json
import logging
import os
import re

logger = logging.getLogger(__name__)

class PropertyService:
    def __init__(self):
        self.properties = self._load_properties()
        self.company_info = self._load_company_info()
    
    def _load_properties(self):
        """Carrega dados dos imóveis"""
        try:
            with open('data/properties.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            logger.warning("Arquivo de imóveis não encontrado, usando dados padrão")
            return []
    
    def _load_company_info(self):
        """Carrega informações da empresa"""
        try:
            with open('data/company_info.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "name": "Nossa Imobiliária",
                "about": "Somos especialistas em encontrar o imóvel perfeito para você!"
            }
    
    def get_property_photos(self, text: str) -> str:
        """Retorna fotos de um imóvel específico"""
        # Detecta código do imóvel (AP001, CA002, etc)
        pattern = r'\\b(AP|CA)\\d{3,4}\\b'
        matches = re.findall(pattern, text.upper())
        
        if not matches:
            return None
        
        property_code = matches[0]
        
        # Busca o imóvel
        for prop in self.properties:
            if prop.get('codigo', '').upper() == property_code:
                response = f"📸 *{prop['tipo']} - {prop['codigo']}*\\n"
                response += f"📍 {prop.get('bairro', '')}, {prop.get('cidade', '')}\\n\\n"
                
                # Adiciona fotos se existirem
                fotos = prop.get('fotos', [])
                if fotos:
                    response += f"🖼️ *{len(fotos)} fotos disponíveis:*\\n\\n"
                    for i, foto_url in enumerate(fotos, 1):
                        response += f"📷 Foto {i}: {foto_url}\\n"
                else:
                    response += "Desculpe, ainda não temos fotos deste imóvel disponíveis.\\n"
                
                # Adiciona tour virtual se existir
                tour = prop.get('tour_virtual')
                if tour:
                    response += f"\\n🎥 *Tour Virtual 360°:*\\n{tour}\\n"
                
                response += f"\\n💰 Valor: R$ {prop.get('preco', 'Consulte')}\\n"
                response += "\\n📱 Interessado? Posso agendar uma visita!"
                
                return response
        
        return f"Desculpe, não encontrei fotos para o imóvel {property_code}."
    
    def search_properties(self, params: dict) -> str:
        """Busca imóveis com base nos parâmetros"""
        results = self.properties
        
        # Aplica filtros
        if params.get('tipo'):
            results = [p for p in results if p['tipo'].lower() == params['tipo'].lower()]
        
        if params.get('operacao'):
            results = [p for p in results if p['operacao'].lower() == params['operacao'].lower()]
        
        if params.get('localizacao'):
            loc = params['localizacao'].lower()
            results = [p for p in results if loc in p.get('bairro', '').lower() or loc in p.get('cidade', '').lower()]
        
        if params.get('quartos'):
            try:
                quartos = int(params['quartos'])
                results = [p for p in results if p.get('quartos', 0) >= quartos]
            except:
                pass
        
        # Formata resposta
        if not results:
            return f"🔍 Não encontrei imóveis com essas características.\\n\\nPosso ajudar com outras opções? Me conte o que você procura!"
        
        response = f"🏠 Encontrei {len(results)} imóve{'l' if len(results) == 1 else 'is'} para você:\\n\\n"
        
        for prop in results[:3]:  # Mostra até 3
            response += f"📍 *{prop['tipo']} - {prop['codigo']}*\\n"
            response += f"📌 {prop.get('bairro', '')}, {prop.get('cidade', '')}\\n"
            response += f"🛏️ {prop.get('quartos', 0)} quartos"
            if prop.get('suites', 0) > 0:
                response += f" ({prop['suites']} suíte{'s' if prop['suites'] > 1 else ''})"
            response += f"\\n💰 R$ {prop.get('preco', 'Consulte')}\\n"
            response += f"📝 {prop.get('descricao', '')}\\n"
            
            # Menciona se tem fotos
            if prop.get('fotos'):
                response += f"📸 {len(prop.get('fotos', []))} fotos disponíveis\\n"
            
            response += "\\n"
        
        if len(results) > 3:
            response += f"... e mais {len(results) - 3} opções disponíveis!\\n\\n"
        
        response += "📲 Digite o código do imóvel para ver fotos ou mais detalhes!"
        
        return response
    
    def get_company_info(self, info_type: str = None) -> str:
        """Retorna informações da empresa"""
        company_name = self.company_info.get('name', 'Nossa Imobiliária')
        
        if info_type == 'contato':
            contact = self.company_info.get('contact', {})
            return f"""📞 *Contatos - {company_name}*

📱 Telefone: {contact.get('phone', 'Não disponível')}
📧 E-mail: {contact.get('email', 'Não disponível')}
📍 Endereço: {contact.get('address', 'Consulte nossos canais')}
🕐 Horário: {contact.get('hours', 'Segunda a Sexta: 9h às 18h')}

Como posso ajudar você hoje?"""
        
        elif info_type == 'financiamento':
            financing = self.company_info.get('financing', 'Oferecemos as melhores condições de financiamento do mercado!')
            return f"""💳 *Financiamento - {company_name}*

{financing}

📋 Documentos necessários:
• RG e CPF
• Comprovante de renda
• Comprovante de residência

Quer simular um financiamento? Me conte sobre o imóvel dos seus sonhos!"""
        
        else:
            about = self.company_info.get('about', 'Somos especialistas em realizar sonhos!')
            return f"""🏢 *Sobre a {company_name}*

{about}

Nossa missão é encontrar o imóvel perfeito para você!

Como posso ajudar em sua busca hoje?"""
    
    def get_sales_script(self) -> str:
        """Retorna script de vendas"""
        return """📝 *Script de Vendas Eficaz*

1️⃣ *Abertura Acolhedora*
"Olá [Nome]! Como está? Vi que você tem interesse em [tipo de imóvel]..."

2️⃣ *Descoberta de Necessidades*
"Para encontrar o imóvel perfeito, me conta: o que é essencial para você?"

3️⃣ *Apresentação Direcionada*
"Baseado no que você me disse, tenho opções incríveis que..."

4️⃣ *Criação de Valor*
"Além do imóvel, oferecemos [diferenciais da empresa]..."

5️⃣ *Fechamento Consultivo*
"Qual dos imóveis mais chamou sua atenção? Quando podemos agendar uma visita?"

💡 *Dicas Extras:*
• Escute mais do que fale
• Personalize sempre a abordagem
• Crie urgência sem pressionar
• Acompanhe pós-venda

Quer praticar com situações específicas?"""
'''
    
    # Salvar atualização
    with open('services/property_service.py', 'w', encoding='utf-8') as f:
        f.write(property_service_update)
    print("✅ property_service.py atualizado!")
    
    # 3. Atualizar message_handler.py
    message_handler_update = '''import logging
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
'''

    # Salvar message_handler
    with open('handlers/message_handler.py', 'w', encoding='utf-8') as f:
        f.write(message_handler_update)
    print("✅ message_handler.py atualizado!")
    
    print("\n🎉 SUPORTE A FOTOS ATIVADO!")
    print("\n📸 Agora teste estas perguntas:")
    print('- "Tem fotos do AP001?"')
    print('- "Quero ver imagens do AP003"')
    print('- "Tem tour virtual?"')
    print('- "Me mostra as fotos da casa CA002"')
    print("\n🚀 Reinicie o bot para aplicar as mudanças!")

if __name__ == "__main__":
    fix_photo_support()
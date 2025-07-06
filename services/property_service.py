import json
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
        pattern = r'\b((?:AP|CA)\d{3,4})\b'
        matches = re.findall(pattern, text.upper())
        
        if not matches:
            return None
        
        property_code = matches[0]
        
        # Busca o imóvel
        for prop in self.properties:
            if prop.get('codigo', '').upper() == property_code:
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
            return f"🔍 Não encontrei imóveis com essas características.\n\nPosso ajudar com outras opções? Me conte o que você procura!"
        
        response = f"🏠 Encontrei {len(results)} imóve{'l' if len(results) == 1 else 'is'} para você:\n\n"
        
        for prop in results[:3]:  # Mostra até 3
            response += f"📍 *{prop['tipo']} - {prop['codigo']}*\n"
            response += f"📌 {prop.get('bairro', '')}, {prop.get('cidade', '')}\n"
            response += f"🛏️ {prop.get('quartos', 0)} quartos"
            if prop.get('suites', 0) > 0:
                response += f" ({prop['suites']} suíte{'s' if prop['suites'] > 1 else ''})"
            response += f"\n💰 R$ {prop.get('preco', 'Consulte')}\n"
            response += f"📝 {prop.get('descricao', '')}\n"
            
            # Menciona se tem fotos
            if prop.get('fotos'):
                response += f"📸 {len(prop.get('fotos', []))} fotos disponíveis\n"
            
            response += "\n"
        
        if len(results) > 3:
            response += f"... e mais {len(results) - 3} opções disponíveis!\n\n"
        
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

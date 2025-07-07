#!/usr/bin/env python3
"""
CORREÇÃO FINAL - Bot com busca por cidade funcionando
Execute: python fix_city_search.py
"""

import os

def fix_city_search():
    
    # MESSAGE HANDLER CORRIGIDO
    fixed_handler = '''import logging
import re
import random
from datetime import datetime
from services.ai_service import AIService
from services.property_service import PropertyService
from utils.emojis import e

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.property_service = PropertyService()
        self.conversations = {}
        
    def process_message(self, text, from_number):
        try:
            if from_number not in self.conversations:
                self.conversations[from_number] = {
                    'history': [],
                    'preferences': {},
                    'name': None,
                    'last_search': None,
                    'context': None
                }
            
            conv = self.conversations[from_number]
            conv['history'].append({'user': text, 'time': datetime.now()})
            
            response = self._process_with_context(text, conv)
            
            # Garante que response é string
            if isinstance(response, dict):
                response_text = response.get('text', 'Desculpe, erro ao processar.')
            else:
                response_text = response if response else 'Desculpe, erro ao processar.'
            
            conv['history'].append({'bot': response_text, 'time': datetime.now()})
            
            return response
            
        except Exception as e:
            logger.error(f"Erro: {e}", exc_info=True)
            return self._error_response()
    
    def _process_with_context(self, text, conv):
        text_lower = text.lower()
        
        # Primeira interação
        if len(conv['history']) <= 1:
            return self._first_interaction()
        
        # Saudações
        if any(word in text_lower for word in ['oi', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
            return self._greeting_response()
        
        # DETECÇÃO DE CIDADE
        city_request = self._extract_city(text)
        if city_request:
            return self._handle_city_search(city_request, text, conv)
        
        # Análise de preço
        price_request = self._extract_price_request(text)
        if price_request:
            return self._handle_price_search(price_request, conv)
        
        # Busca geral
        if self._is_property_search(text):
            return self._smart_search(text, conv)
        
        # Código de imóvel
        property_code = self._extract_property_code(text)
        if property_code:
            return self._show_property_details(property_code, conv)
        
        # Fotos
        if any(word in text_lower for word in ['foto', 'imagem', 'ver', 'mostra']):
            return self._handle_photo_request(text, conv)
        
        # Conversação geral
        return self._contextual_response(text, conv)
    
    def _extract_city(self, text):
        """Extrai menção a cidades"""
        text_lower = text.lower()
        
        # Lista de cidades conhecidas
        cities = {
            'florianópolis': ['florianopolis', 'floripa', 'ilha'],
            'palhoça': ['palhoca', 'palhaça'],
            'são josé': ['sao jose', 'são jose'],
            'biguaçu': ['biguacu'],
            'porto alegre': ['porto alegre', 'poa'],
            'curitiba': ['curitiba', 'ctba'],
            'são paulo': ['sao paulo', 'são paulo', 'sp'],
            'rio de janeiro': ['rio de janeiro', 'rio', 'rj']
        }
        
        for city, variations in cities.items():
            if city in text_lower:
                return city
            for variation in variations:
                if variation in text_lower:
                    return city
        
        return None
    
    def _handle_city_search(self, city, text, conv):
        """Busca por cidade com resposta precisa"""
        # Extrai outras preferências
        preferences = self._extract_preferences(text)
        preferences['cidade'] = city
        
        # Busca imóveis
        properties = self.property_service.search_with_preferences(preferences)
        
        # Filtra por cidade
        city_properties = [p for p in properties if p.get('cidade', 'florianópolis').lower() == city.lower()]
        
        if not city_properties:
            return self._no_properties_in_city(city, properties, preferences)
        
        # Resposta com imóveis da cidade
        response = f"Sim! Temos {len(city_properties)} {'imóvel' if len(city_properties) == 1 else 'imóveis'} em {city.title()}:\\n\\n"
        
        for i, prop in enumerate(city_properties[:5], 1):
            response += f"{i}. {prop['tipo']} em {prop['bairro']}\\n"
            response += f"   {e('money')} R$ {prop['preco']}\\n"
            response += f"   {e('casa')} {prop['quartos']} quartos\\n"
            if prop.get('destaque'):
                response += f"   {e('star')} {prop['destaque']}\\n"
            response += f"   {e('key')} Código: {prop['codigo']}\\n\\n"
        
        response += f"\\n{e('bulb')} Digite o código para ver mais detalhes!"
        
        # Salva contexto
        conv['preferences'] = preferences
        conv['last_search'] = f"imoveis em {city}"
        
        return response
    
    def _no_properties_in_city(self, city, all_properties, preferences):
        """Resposta quando não tem imóveis na cidade"""
        response = f"Desculpe, não temos imóveis em {city.title()} no momento. {e('thinking')}\\n\\n"
        
        # Sugere cidades próximas onde tem imóveis
        available_cities = set()
        for prop in all_properties:
            city_name = prop.get('cidade', 'Florianópolis')
            available_cities.add(city_name)
        
        if available_cities:
            response += "Mas temos excelentes opções em:\\n"
            for available_city in list(available_cities)[:3]:
                city_count = len([p for p in all_properties if p.get('cidade', 'Florianópolis') == available_city])
                response += f"• {available_city} ({city_count} {'imóvel' if city_count == 1 else 'imóveis'})\\n"
            
            response += f"\\nQuer ver as opções em {list(available_cities)[0]}?"
        
        return response
    
    def _extract_price_request(self, text):
        """Extrai pedidos de preço"""
        text_lower = text.lower()
        
        patterns = [
            r'abaixo de (\\d+)',
            r'menos de (\\d+)',
            r'até (\\d+)',
            r'menor que (\\d+)',
            r'maximo (\\d+)',
            r'máximo (\\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower.replace('.', '').replace('mil', '000').replace(' ', ''))
            if match:
                return {'max_price': int(match.group(1)), 'type': 'max'}
        
        return None
    
    def _handle_price_search(self, price_request, conv):
        """Busca por preço"""
        max_price = price_request.get('max_price', 0)
        
        preferences = conv.get('preferences', {}).copy()
        preferences['max_price'] = max_price
        
        properties = self.property_service.search_by_price(preferences)
        
        if not properties:
            return self._no_results_for_price(max_price, conv)
        
        response = f"Encontrei {len(properties)} {'imóvel' if len(properties) == 1 else 'imóveis'} "
        response += f"abaixo de R$ {max_price:,.0f}:\\n\\n"
        
        for i, prop in enumerate(properties[:5], 1):
            response += f"{i}. {prop['tipo']} em {prop['bairro']}\\n"
            response += f"   {e('money')} R$ {prop['preco']}\\n"
            response += f"   {e('casa')} {prop['quartos']} quartos\\n"
            response += f"   {e('key')} Código: {prop['codigo']}\\n\\n"
        
        response += f"{e('bulb')} Digite o código para ver detalhes!"
        
        conv['preferences'] = preferences
        
        return response
    
    def _no_results_for_price(self, max_price, conv):
        """Quando não há resultados para o preço"""
        all_properties = self.property_service.get_all_properties()
        
        if not all_properties:
            return f"Desculpe, não encontrei imóveis no momento. {e('thinking')}"
        
        cheapest = min(all_properties, key=lambda x: self._parse_price(x.get('preco', '999999999')))
        cheapest_price = self._parse_price(cheapest.get('preco', '999999999'))
        
        response = f"Não encontrei imóveis abaixo de R$ {max_price:,.0f}. {e('thinking')}\\n\\n"
        response += f"O mais em conta que temos é:\\n\\n"
        response += f"{e('sparkles')} {cheapest['tipo']} em {cheapest['bairro']}\\n"
        response += f"{e('money')} R$ {cheapest['preco']}\\n"
        response += f"{e('casa')} {cheapest['quartos']} quartos\\n"
        response += f"{e('key')} Código: {cheapest['codigo']}\\n\\n"
        response += "Posso mostrar opções de financiamento?"
        
        return response
    
    def _parse_price(self, price_str):
        """Converte preço para número"""
        try:
            if not price_str:
                return 999999999
            clean = str(price_str).replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(clean)
        except:
            return 999999999
    
    def _is_property_search(self, text):
        text_lower = text.lower()
        search_words = ['procuro', 'quero', 'preciso', 'busco', 'tem', 'existe',
                       'apartamento', 'casa', 'kitnet', 'cobertura',
                       'comprar', 'alugar', 'quartos', 'bairro']
        return any(word in text_lower for word in search_words)
    
    def _smart_search(self, text, conv):
        """Busca inteligente"""
        preferences = self._extract_preferences(text)
        
        # Mantém preferências anteriores
        if conv.get('preferences'):
            base_prefs = conv['preferences'].copy()
            base_prefs.update(preferences)
            preferences = base_prefs
        
        conv['preferences'] = preferences
        conv['last_search'] = text
        
        properties = self.property_service.search_with_preferences(preferences)
        
        if not properties:
            return self._no_results_response(conv)
        
        understood = self._explain_search(preferences)
        
        response = f"{understood}\\n\\n"
        response += f"Encontrei {len(properties)} {'opção' if len(properties) == 1 else 'opções'}:\\n\\n"
        
        for i, prop in enumerate(properties[:5], 1):
            response += f"{i}. {prop['tipo']} em {prop['bairro']}\\n"
            response += f"   {e('money')} R$ {prop['preco']}\\n"
            response += f"   {e('casa')} {prop['quartos']} quartos\\n"
            if prop.get('destaque'):
                response += f"   {e('star')} {prop['destaque']}\\n"
            response += f"   {e('key')} Código: {prop['codigo']}\\n\\n"
        
        response += f"\\n{e('bulb')} Digite o código para ver detalhes!"
        
        return response
    
    def _explain_search(self, preferences):
        """Explica o que entendeu"""
        parts = []
        
        if preferences.get('tipo'):
            parts.append(preferences['tipo'])
        
        if preferences.get('operacao'):
            parts.append(f"para {preferences['operacao']}")
        
        if preferences.get('quartos'):
            parts.append(f"com {preferences['quartos']}+ quartos")
        
        if preferences.get('cidade'):
            parts.append(f"em {preferences['cidade']}")
        
        if preferences.get('bairro'):
            parts.append(f"no {preferences['bairro']}")
        
        if preferences.get('max_price'):
            parts.append(f"até R$ {preferences['max_price']:,.0f}")
        
        if parts:
            return f"Entendi! Você busca {' '.join(parts)}."
        else:
            return "Vou mostrar todas as opções disponíveis:"
    
    def _show_property_details(self, code, conv):
        """Mostra detalhes do imóvel"""
        prop = self.property_service.get_property_details(code)
        
        if not prop:
            all_codes = self.property_service.get_all_codes()
            similar = [c for c in all_codes if c.startswith(code[:2])]
            
            if similar:
                return f"Não encontrei {code}. Você quis dizer {' ou '.join(similar[:3])}?"
            else:
                return f"Código {code} não encontrado. Tente AP001, AP003, AP005, CA002 ou CA004."
        
        response = f"{e('casa')} **{prop['tipo']} - {prop['codigo']}**\\n"
        response += f"{e('location')} {prop['bairro']}, {prop.get('cidade', 'Florianópolis')}\\n\\n"
        response += f"{prop['descricao']}\\n\\n"
        response += f"{e('money')} **Valor:** R$ {prop['preco']}\\n"
        response += f"🛏️ **Quartos:** {prop['quartos']}\\n"
        
        if prop.get('suites'):
            response += f"🚿 **Suítes:** {prop['suites']}\\n"
        
        if prop.get('area'):
            response += f"📐 **Área:** {prop['area']}m²\\n"
        
        if prop.get('vagas'):
            response += f"🚗 **Vagas:** {prop['vagas']}\\n"
        
        response += f"\\n📸 Digite 'fotos' para ver imagens"
        response += f"\\n📅 Digite 'visitar' para agendar visita"
        
        conv['context'] = {'viewing': code}
        
        return response
    
    def _handle_photo_request(self, text, conv):
        """Mostra fotos"""
        context = conv.get('context', {})
        viewing = context.get('viewing')
        
        if not viewing:
            # Tenta encontrar código no histórico
            for msg in reversed(conv.get('history', [])):
                if 'bot' in msg:
                    code = self._extract_property_code(str(msg.get('bot', '')))
                    if code:
                        viewing = code
                        break
        
        if not viewing:
            return "Qual imóvel você quer ver as fotos? Me passe o código (ex: AP001)."
        
        photos = self.property_service.get_property_photos_list(viewing)
        
        if photos:
            return {
                "text": f"Fotos do {viewing}:",
                "media": photos[:3]
            }
        else:
            return f"Ainda não temos fotos do {viewing}, mas posso agendar uma visita! Digite 'visitar'."
    
    def _first_interaction(self):
        return f"""Olá! Sou o Tony, seu assistente imobiliário! {e('wave')}

Como posso ajudar?
- Buscar imóveis para comprar ou alugar
- Filtrar por preço, quartos, bairro
- Ver fotos e agendar visitas

O que você procura hoje?"""
    
    def _greeting_response(self):
        greetings = [
            f"Oi! Como posso ajudar você hoje? {e('smile')}",
            f"Olá! Em que posso ajudar? {e('wave')}",
            f"Oi! Procurando um imóvel? {e('casa')}"
        ]
        return random.choice(greetings)
    
    def _contextual_response(self, text, conv):
        """Resposta contextual"""
        if conv.get('context', {}).get('viewing'):
            code = conv['context']['viewing']
            return f"Ainda vendo o {code}? Digite 'fotos' ou 'visitar'!"
        
        return f"Não entendi bem. Você pode:\\n• Buscar: 'quero apartamento'\\n• Cidade: 'tem em Palhoça?'\\n• Preço: 'abaixo de 500 mil'\\n• Código: 'AP001'\\n\\nComo posso ajudar? {e('smile')}"
    
    def _no_results_response(self, conv):
        """Quando não há resultados"""
        criteria = conv.get('preferences', {})
        
        response = f"Não encontrei imóveis com esses critérios. {e('thinking')}\\n\\n"
        
        if criteria:
            response += "Sugestões:\\n"
            
            if criteria.get('quartos', 0) > 2:
                response += f"• Tentar com {criteria['quartos']-1} quartos\\n"
            
            if criteria.get('max_price'):
                response += f"• Aumentar o orçamento\\n"
            
            if criteria.get('cidade'):
                response += f"• Ver outras cidades\\n"
        
        response += "\\nQuer ajustar a busca?"
        
        return response
    
    def _error_response(self):
        return f"Ops! Algo deu errado. {e('sweat')} Digite 'oi' para recomeçar!"
    
    def _extract_property_code(self, text):
        if not text:
            return None
        match = re.search(r'\\b(AP|CA)\\d{3,4}\\b', str(text).upper())
        return match.group() if match else None
    
    def _extract_preferences(self, text):
        prefs = {}
        text_lower = text.lower()
        
        # Tipo
        if 'apartamento' in text_lower:
            prefs['tipo'] = 'apartamento'
        elif 'casa' in text_lower:
            prefs['tipo'] = 'casa'
        
        # Operação
        if any(word in text_lower for word in ['comprar', 'compra', 'venda']):
            prefs['operacao'] = 'venda'
        elif any(word in text_lower for word in ['alugar', 'aluguel', 'locar']):
            prefs['operacao'] = 'aluguel'
        
        # Quartos
        quartos_match = re.search(r'(\\d+)\\s*quarto', text_lower)
        if quartos_match:
            prefs['quartos'] = int(quartos_match.group(1))
        
        # Bairro
        bairros = ['centro', 'trindade', 'agronômica', 'campeche', 'jurerê']
        for bairro in bairros:
            if bairro in text_lower:
                prefs['bairro'] = bairro
                break
        
        return prefs
'''

    # SALVAR
    print("Implementando correção de busca por cidade...")
    
    with open('handlers/message_handler.py', 'w', encoding='utf-8') as f:
        f.write(fixed_handler)
    print("[OK] handlers/message_handler.py")
    
    print("\n[SUCESSO] Bot corrigido!")
    print("\nAgora funciona:")
    print("✅ Busca por cidade (Palhoça, Porto Alegre, etc)")
    print("✅ Responde corretamente quando não tem imóveis na cidade")
    print("✅ Corrigido erro 'NoneType'")
    print("✅ Mantém contexto das buscas")
    print("✅ Sugere alternativas quando não encontra")
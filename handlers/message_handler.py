import logging
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
            
            conv['history'].append({'bot': response, 'time': datetime.now()})
            
            return response
            
        except Exception as e:
            logger.error(f"Erro: {e}")
            return self._error_response()
    
    def _process_with_context(self, text, conv):
        text_lower = text.lower()
        
        # Primeira interação
        if len(conv['history']) <= 1:
            return self._first_interaction()
        
        # Saudações
        if any(word in text_lower for word in ['oi', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
            return self._greeting_response()
        
        # ANÁLISE PRECISA DE PREÇO
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
        
        # Perguntas sobre fotos
        if any(word in text_lower for word in ['foto', 'imagem', 'ver', 'mostra']):
            return self._handle_photo_request(text, conv)
        
        # Conversação geral
        return self._contextual_response(text, conv)
    
    def _extract_price_request(self, text):
        """Extrai pedidos relacionados a preço com precisão"""
        text_lower = text.lower()
        
        # Padrões de preço
        patterns = [
            r'abaixo de (\d+)',
            r'menos de (\d+)',
            r'até (\d+)',
            r'menor que (\d+)',
            r'maximo (\d+)',
            r'máximo (\d+)',
            r'no maximo (\d+)',
            r'no máximo (\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower.replace('.', '').replace('mil', '000').replace(' ', ''))
            if match:
                return {
                    'max_price': int(match.group(1)),
                    'type': 'max'
                }
        
        # Faixa de preço
        range_pattern = r'entre (\d+) e (\d+)'
        range_match = re.search(range_pattern, text_lower.replace('.', '').replace('mil', '000').replace(' ', ''))
        if range_match:
            return {
                'min_price': int(range_match.group(1)),
                'max_price': int(range_match.group(2)),
                'type': 'range'
            }
        
        return None
    
    def _handle_price_search(self, price_request, conv):
        """Busca precisa por preço SEM INVENTAR"""
        max_price = price_request.get('max_price', 0)
        min_price = price_request.get('min_price', 0)
        
        # Mantém preferências anteriores
        preferences = conv.get('preferences', {}).copy()
        preferences['max_price'] = max_price
        if min_price:
            preferences['min_price'] = min_price
        
        # Busca imóveis
        properties = self.property_service.search_by_price(preferences)
        
        if not properties:
            return self._no_results_for_price(max_price, conv)
        
        # Resposta precisa
        response = f"Encontrei {len(properties)} {'imóvel' if len(properties) == 1 else 'imóveis'} "
        
        if min_price:
            response += f"entre R$ {min_price:,.0f} e R$ {max_price:,.0f}:\n\n"
        else:
            response += f"abaixo de R$ {max_price:,.0f}:\n\n"
        
        for i, prop in enumerate(properties[:5], 1):
            valor_num = self._parse_price(prop['preco'])
            response += f"{i}. {prop['tipo']} em {prop['bairro']}\n"
            response += f"   {e('money')} R$ {prop['preco']}\n"
            response += f"   {e('casa')} {prop['quartos']} quartos | {prop.get('area', '??')}m²\n"
            response += f"   {e('key')} Código: {prop['codigo']}\n\n"
        
        if len(properties) > 5:
            response += f"... e mais {len(properties) - 5} opções!\n\n"
        
        response += f"{e('bulb')} Digite o código para ver detalhes e fotos!"
        
        # Salva contexto
        conv['preferences'] = preferences
        conv['last_search'] = f"imoveis ate {max_price}"
        
        return response
    
    def _no_results_for_price(self, max_price, conv):
        """Resposta honesta quando não há resultados"""
        # Busca o mais barato disponível
        all_properties = self.property_service.get_all_properties()
        
        if not all_properties:
            return f"Desculpe, não encontrei imóveis no momento. {e('thinking')}"
        
        # Encontra o mais barato
        cheapest = min(all_properties, key=lambda x: self._parse_price(x['preco']))
        cheapest_price = self._parse_price(cheapest['preco'])
        
        response = f"Não encontrei imóveis abaixo de R$ {max_price:,.0f}. {e('thinking')}\n\n"
        
        if cheapest_price < max_price * 1.5:  # Se está relativamente próximo
            response += f"Mas tenho uma opção próxima do seu orçamento:\n\n"
            response += f"{e('sparkles')} {cheapest['tipo']} em {cheapest['bairro']}\n"
            response += f"{e('money')} R$ {cheapest['preco']} (apenas R$ {cheapest_price - max_price:,.0f} acima)\n"
            response += f"{e('casa')} {cheapest['quartos']} quartos\n"
            response += f"{e('key')} Código: {cheapest['codigo']}\n\n"
            response += "Às vezes vale a pena esticar um pouquinho o orçamento! Quer ver?"
        else:
            response += f"O imóvel mais em conta que tenho custa R$ {cheapest['preco']}.\n\n"
            response += "Posso te mostrar algumas opções de financiamento que cabem no seu bolso?"
        
        return response
    
    def _parse_price(self, price_str):
        """Converte string de preço para número"""
        try:
            # Remove R$, pontos e converte vírgula
            clean = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
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
        """Busca inteligente sem inventar dados"""
        preferences = self._extract_preferences(text)
        conv['preferences'].update(preferences)
        conv['last_search'] = text
        
        properties = self.property_service.search_with_preferences(conv['preferences'])
        
        if not properties:
            return self._no_results_response(conv)
        
        # Confirma o que entendeu
        understood = self._explain_search(conv['preferences'])
        
        response = f"{understood}\n\n"
        response += f"Encontrei {len(properties)} {'opção' if len(properties) == 1 else 'opções'}:\n\n"
        
        for i, prop in enumerate(properties[:5], 1):
            response += f"{i}. {prop['tipo']} em {prop['bairro']}\n"
            response += f"   {e('money')} R$ {prop['preco']}\n"
            response += f"   {e('casa')} {prop['quartos']} quartos\n"
            if prop.get('destaque'):
                response += f"   {e('star')} {prop['destaque']}\n"
            response += f"   {e('key')} Código: {prop['codigo']}\n\n"
        
        response += f"\n{e('bulb')} Digite o código para ver detalhes completos!"
        
        return response
    
    def _explain_search(self, preferences):
        """Explica o que entendeu da busca"""
        parts = []
        
        if preferences.get('tipo'):
            parts.append(preferences['tipo'])
        
        if preferences.get('operacao'):
            parts.append(f"para {preferences['operacao']}")
        
        if preferences.get('quartos'):
            parts.append(f"com {preferences['quartos']}+ quartos")
        
        if preferences.get('max_price'):
            parts.append(f"até R$ {preferences['max_price']:,.0f}")
        
        if preferences.get('bairro'):
            parts.append(f"em {preferences['bairro']}")
        
        if parts:
            return f"Entendi! Você busca {' '.join(parts)}."
        else:
            return "Vou mostrar todas as opções disponíveis:"
    
    def _show_property_details(self, code, conv):
        """Mostra detalhes REAIS do imóvel"""
        prop = self.property_service.get_property_details(code)
        
        if not prop:
            # Busca códigos similares
            all_codes = self.property_service.get_all_codes()
            similar = [c for c in all_codes if c.startswith(code[:2])]
            
            if similar:
                return f"Não encontrei {code}. Você quis dizer {' ou '.join(similar[:3])}?"
            else:
                return f"Código {code} não encontrado. Digite 'ajuda' para ver os códigos disponíveis."
        
        response = f"{e('casa')} **{prop['tipo']} - {prop['codigo']}**\n"
        response += f"{e('location')} {prop['bairro']}, {prop.get('cidade', 'Florianópolis')}\n\n"
        response += f"{prop['descricao']}\n\n"
        response += f"{e('money')} **Valor:** R$ {prop['preco']}\n"
        response += f"🛏️ **Quartos:** {prop['quartos']}\n"
        
        if prop.get('suites'):
            response += f"🚿 **Suítes:** {prop['suites']}\n"
        
        if prop.get('area'):
            response += f"📐 **Área:** {prop['area']}m²\n"
        
        if prop.get('vagas'):
            response += f"🚗 **Vagas:** {prop['vagas']}\n"
        
        response += f"\n📸 Digite 'fotos' para ver imagens"
        response += f"\n📅 Digite 'visitar' para agendar visita"
        
        conv['context'] = {'viewing': code}
        
        return response
    
    def _handle_photo_request(self, text, conv):
        """Mostra fotos se existirem"""
        context = conv.get('context', {})
        viewing = context.get('viewing')
        
        if not viewing:
            return "Qual imóvel você quer ver as fotos? Me passe o código."
        
        photos = self.property_service.get_property_photos_list(viewing)
        
        if photos:
            return {
                "text": f"Fotos do {viewing}:",
                "media": photos[:3]
            }
        else:
            return f"Ainda não temos fotos do {viewing}, mas posso agendar uma visita presencial!"
    
    def _first_interaction(self):
        return f"""Olá! Sou o Tony, seu assistente imobiliário! {e('wave')}

Como posso ajudar?
- Buscar imóveis para comprar ou alugar
- Filtrar por preço, quartos, bairro
- Ver fotos e agendar visitas

O que você procura hoje?"""
    
    def _greeting_response(self):
        return f"Oi! Como posso ajudar você hoje? {e('smile')}"
    
    def _contextual_response(self, text, conv):
        """Resposta contextual sem inventar"""
        # Se tem contexto de visualização
        if conv.get('context', {}).get('viewing'):
            code = conv['context']['viewing']
            return f"Ainda está vendo o {code}? Digite 'fotos' para ver imagens ou 'visitar' para agendar!"
        
        # Resposta genérica
        return f"Não entendi bem. Você pode:\n• Buscar: 'quero apartamento 2 quartos'\n• Filtrar: 'abaixo de 500 mil'\n• Ver código: 'AP001'\n\nComo posso ajudar? {e('smile')}"
    
    def _no_results_response(self, conv):
        """Resposta honesta quando não há resultados"""
        criteria = conv.get('preferences', {})
        
        response = f"Não encontrei imóveis com todos esses critérios. {e('thinking')}\n\n"
        
        # Sugere relaxar filtros
        if criteria.get('quartos') and criteria.get('quartos') > 2:
            response += f"• Tenho opções com {criteria['quartos']-1} quartos\n"
        
        if criteria.get('max_price'):
            response += f"• Ou com preços um pouco acima de R$ {criteria['max_price']:,.0f}\n"
        
        response += "\nQuer ajustar a busca?"
        
        return response
    
    def _error_response(self):
        return f"Ops! Algo deu errado. {e('sweat')} Digite 'oi' para recomeçar!"
    
    def _extract_property_code(self, text):
        match = re.search(r'\b(AP|CA)\d{3,4}\b', text.upper())
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
        quartos_match = re.search(r'(\d+)\s*quarto', text_lower)
        if quartos_match:
            prefs['quartos'] = int(quartos_match.group(1))
        
        # Bairro
        bairros = ['centro', 'trindade', 'agronômica', 'campeche', 'jurerê']
        for bairro in bairros:
            if bairro in text_lower:
                prefs['bairro'] = bairro
                break
        
        return prefs

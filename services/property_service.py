import json
import logging
import re

logger = logging.getLogger(__name__)

class PropertyService:
    def __init__(self):
        self.properties = self._load_properties()
        self._enhance_properties()
    
    def _load_properties(self):
        try:
            with open('data/properties.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            logger.warning("Arquivo de imóveis não encontrado")
            return []
    
    def _enhance_properties(self):
        """Adiciona dados extras aos imóveis"""
        enhancements = {
            'AP001': {'area': '120', 'vagas': '2', 'destaque': 'Vista Mar'},
            'CA002': {'area': '350', 'vagas': '4', 'destaque': 'Condomínio Fechado'},
            'AP003': {'area': '65', 'vagas': '1', 'destaque': 'Mobiliado'},
            'CA004': {'area': '180', 'vagas': '2', 'destaque': 'Perto da Praia'},
            'AP005': {'area': '75', 'vagas': '1', 'destaque': 'Novo'}
        }
        
        for prop in self.properties:
            code = prop.get('codigo')
            if code in enhancements:
                prop.update(enhancements[code])
    
    def search_by_price(self, preferences):
        """Busca PRECISA por preço"""
        results = self.properties.copy()
        
        # Filtros básicos primeiro
        if preferences.get('tipo'):
            results = [p for p in results if p['tipo'].lower() == preferences['tipo'].lower()]
        
        if preferences.get('operacao'):
            results = [p for p in results if p['operacao'].lower() == preferences['operacao'].lower()]
        
        # FILTRO DE PREÇO PRECISO
        max_price = preferences.get('max_price')
        min_price = preferences.get('min_price', 0)
        
        if max_price:
            filtered = []
            for prop in results:
                prop_price = self._parse_price(prop['preco'])
                if min_price <= prop_price <= max_price:
                    filtered.append(prop)
            results = filtered
        
        # Ordena por preço
        results = sorted(results, key=lambda x: self._parse_price(x['preco']))
        
        return results
    
    def search_with_preferences(self, preferences):
        """Busca geral com preferências"""
        results = self.properties.copy()
        
        # Tipo
        if preferences.get('tipo'):
            results = [p for p in results if p['tipo'].lower() == preferences['tipo'].lower()]
        
        # Operação
        if preferences.get('operacao'):
            results = [p for p in results if p['operacao'].lower() == preferences['operacao'].lower()]
        
        # Quartos
        if preferences.get('quartos'):
            min_quartos = preferences['quartos']
            results = [p for p in results if p.get('quartos', 0) >= min_quartos]
        
        # Bairro
        if preferences.get('bairro'):
            bairro = preferences['bairro'].lower()
            results = [p for p in results if bairro in p.get('bairro', '').lower()]
        
        # Preço
        if preferences.get('max_price'):
            results = self.search_by_price(preferences)
        
        return results
    
    def get_property_details(self, code):
        """Retorna detalhes do imóvel ou None"""
        for prop in self.properties:
            if prop.get('codigo', '').upper() == code.upper():
                return prop
        return None
    
    def get_property_photos_list(self, code):
        """Retorna fotos se existirem"""
        prop = self.get_property_details(code)
        if prop:
            return prop.get('fotos', [])
        return []
    
    def get_all_properties(self):
        """Retorna todos os imóveis"""
        return self.properties
    
    def get_all_codes(self):
        """Retorna todos os códigos disponíveis"""
        return [p.get('codigo', '') for p in self.properties if p.get('codigo')]
    
    def _parse_price(self, price_str):
        """Converte preço string para float"""
        try:
            clean = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(clean)
        except:
            return 999999999

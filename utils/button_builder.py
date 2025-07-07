class ButtonBuilder:
    """Constrói botões interativos para WhatsApp"""
    
    def get_main_menu(self) -> list:
        """Menu principal"""
        return [
            {"id": "search_buy", "title": "🏠 Comprar Imóvel"},
            {"id": "search_rent", "title": "🔑 Alugar Imóvel"},
            {"id": "contact", "title": "📞 Falar com Corretor"}
        ]
    
    def get_search_options(self) -> list:
        """Opções de busca"""
        return [
            {"id": "new_search", "title": "🔍 Nova Busca"},
            {"id": "filter_price", "title": "💰 Filtrar Preço"},
            {"id": "main_menu", "title": "🏠 Menu Principal"}
        ]
    
    def get_property_actions(self, property_code: str) -> list:
        """Ações para um imóvel"""
        return [
            {"id": f"photos_{property_code}", "title": "📸 Ver Fotos"},
            {"id": f"schedule_{property_code}", "title": "📅 Agendar Visita"},
            {"id": "see_more", "title": "🔍 Ver Mais"}
        ]
    
    def get_current_options(self, context: dict) -> list:
        """Opções baseadas no contexto atual"""
        flow = context.get('current_flow', '')
        
        if flow == 'viewing_properties':
            return self.get_property_actions(context.get('viewing_property', 'AP001'))
        elif flow == 'search':
            return self.get_search_options()
        else:
            return self.get_main_menu()
    
    def get_contextual_buttons(self, text: str) -> list:
        """Botões contextuais baseados no texto"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['comprar', 'venda', 'compra']):
            return [{"id": "search_buy", "title": "🏠 Ver Imóveis à Venda"}]
        elif any(word in text_lower for word in ['alugar', 'aluguel', 'locação']):
            return [{"id": "search_rent", "title": "🔑 Ver Imóveis para Alugar"}]
        else:
            return self.get_main_menu()

class DemoMode:
    def __init__(self):
        self.active = False
        self.stats = {
            "total_conversations": 15847,
            "satisfaction_rate": 94.8,
            "average_response_time": 1.2,
            "conversion_rate": 32.5,
            "properties_shown": 48392,
            "appointments_scheduled": 4821
        }
    
    def activate(self) -> str:
        """Ativa o modo demonstração"""
        self.active = True
        return """🎯 *MODO DEMONSTRAÇÃO ATIVADO*

📊 *Estatísticas Impressionantes:*
• 15.847 conversas processadas
• 94.8% de satisfação dos clientes
• 1.2s tempo médio de resposta
• 32.5% taxa de conversão
• 48.392 imóveis apresentados
• 4.821 visitas agendadas

🤖 *Capacidades Especiais:*
• Transcrição de áudio em 12 idiomas
• Análise de sentimento em tempo real
• Integração com 8 sistemas de CRM
• Machine Learning para recomendações
• Disponível 24/7 sem interrupções

Digite 'demo off' para sair do modo demonstração."""
    
    def get_enhanced_response(self, original_response: str) -> str:
        """Melhora a resposta no modo demo"""
        if not self.active:
            return original_response
        
        enhancements = [
            "\n\n💡 *Insight IA:* Com base no seu perfil, você tem 87% de chance de gostar deste imóvel!",
            "\n\n📈 *Análise de Mercado:* Este imóvel está 12% abaixo do valor médio da região.",
            "\n\n🏆 *Recomendação Premium:* Este é um dos TOP 5 imóveis mais procurados esta semana!",
            "\n\n🔥 *Alerta:* 3 outras pessoas visualizaram este imóvel nas últimas 2 horas."
        ]
        
        import random
        return original_response + random.choice(enhancements)

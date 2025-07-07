from typing import Dict

class ExcuseHandler:
    """Converte objeções em oportunidades"""
    
    def __init__(self):
        self.responses = {
            'caro': {
                'immediate': """Entendo perfeitamente! Mas veja só:
                
💡 Aluguel na região: R$ 2.500/mês (jogando dinheiro fora)
🏠 Parcela do financiamento: R$ 2.300/mês (construindo patrimônio)
📈 Você ECONOMIZA R$ 200/mês e ainda fica com um imóvel!

Quer ver a simulação completa? É impressionante!""",
                'followup': "Descobri uma condição especial do banco: entrada parcelada em 12x!"
            },
            
            'pensar': {
                'immediate': """Claro, decisão importante! 

Enquanto você pensa, vou fazer algo especial:
✅ Reservei o imóvel por 48h no seu nome
✅ Ninguém mais pode visitar neste período
✅ Preparei uma análise comparativa

Que tal conversarmos amanhã às 19h? Tiro todas suas dúvidas!""",
                'followup': "A reserva do apartamento termina hoje às 18h. Conseguiu pensar?"
            },
            
            'outros': {
                'immediate': """Perfeito! Aliás, ADOREI sua atitude de pesquisar! 

Fiz algo para te ajudar:
📊 Comparativo deste com 5 similares
✅ Prós e contras de cada um
💰 Análise de custo-benefício

Envio agora! Mas já adianto: esse tem o melhor custo-benefício da região.""",
                'followup': "E aí, como foram as outras visitas? Conseguiu comparar?"
            },
            
            'conjuge': {
                'immediate': """Fundamental mesmo! Decisão do casal! 

Tenho uma ideia:
📱 Posso fazer um tour virtual por vídeo AGORA?
📸 Ou preparar um dossiê completo com fotos HD
🎥 Temos tour 360° que vocês podem ver juntos

O que prefere? Quero que ambos se apaixonem!""",
                'followup': "Oi! O proprietário fez uma proposta especial: móveis planejados de brinde para decisão essa semana!"
            },
            
            'momento': {
                'immediate': """Compreendo totalmente! Timing é tudo! 

Que tal isso:
🌟 Te adiciono na lista VIP de lançamentos
📱 Você recebe em primeira mão as oportunidades
💎 Quando chegar a hora, terá as melhores opções

E se eu te mostrar algo que pode ANTECIPAR seus planos?""",
                'followup': "Apareceu algo MUITO especial que lembrei de você. Mudou de ideia sobre o timing?"
            }
        }
    
    def handle(self, excuse_type: str, user_id: str) -> str:
        """Retorna resposta para a objeção"""
        
        if excuse_type in self.responses:
            return self.responses[excuse_type]['immediate']
        
        # Resposta genérica
        return """Entendo sua preocupação! 

Me conta: o que tornaria este imóvel PERFEITO para você?

Às vezes consigo negociar condições especiais! 😊"""
    
    def get_followup(self, excuse_type: str) -> str:
        """Retorna mensagem de follow-up"""
        
        if excuse_type in self.responses:
            return self.responses[excuse_type]['followup']
        
        return "Oi! Lembrei de você. Conseguiu pensar melhor sobre o imóvel?"

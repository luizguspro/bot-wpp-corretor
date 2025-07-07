import json
from datetime import datetime, timedelta
from typing import Dict, List

class LeadScorer:
    """Sistema de pontuação de leads em tempo real"""
    
    def __init__(self):
        self.scores = {}
        self.hot_signals = {
            'urgency': ['urgente', 'hoje', 'rápido', 'preciso', 'imediato', 'agora'],
            'commitment': ['comprar', 'fechar', 'decidir', 'quanto entrada', 'financiamento'],
            'family': ['esposa', 'marido', 'família', 'filhos', 'mudança', 'casando'],
            'specific': ['gostei', 'perfeito', 'é esse', 'quero esse', 'adorei'],
            'viewing': ['visitar', 'ver', 'conhecer', 'quando posso', 'marcar'],
            'budget': ['valor', 'preço', 'quanto', 'entrada', 'parcela', 'à vista']
        }
    
    def analyze_lead(self, user_id: str, conversation_history: List[Dict]) -> Dict:
        """Analisa e pontua o lead"""
        
        score = 0
        signals_found = []
        
        # Analisa cada mensagem
        for msg in conversation_history:
            if msg.get('from') == 'user':
                text = msg.get('text', '').lower()
                
                # Busca sinais quentes
                for category, keywords in self.hot_signals.items():
                    for keyword in keywords:
                        if keyword in text:
                            score += 10
                            signals_found.append(f"{category}: {keyword}")
        
        # Fatores comportamentais
        if len(conversation_history) > 5:
            score += 15  # Conversa longa
            signals_found.append("engagement: conversa longa")
        
        # Velocidade de resposta
        response_times = self._calculate_response_times(conversation_history)
        if response_times and sum(response_times) / len(response_times) < 120:
            score += 10  # Responde rápido
            signals_found.append("engagement: respostas rápidas")
        
        # Classificação
        if score >= 80:
            classification = "🔥 QUENTE - FECHAR AGORA!"
            action = "Ligar imediatamente"
        elif score >= 60:
            classification = "🟡 MORNO - NUTRIR"
            action = "Enviar opções personalizadas"
        elif score >= 40:
            classification = "🔵 FRIO - ACOMPANHAR"
            action = "Follow-up em 3 dias"
        else:
            classification = "❄️ GELADO - AUTOMAÇÃO"
            action = "Manter em campanha de email"
        
        # Salva score
        self.scores[user_id] = {
            'score': min(score, 100),
            'classification': classification,
            'signals': list(set(signals_found))[:5],
            'last_updated': datetime.now()
        }
        
        return {
            'score': min(score, 100),
            'classification': classification,
            'signals': list(set(signals_found))[:5],
            'action': action,
            'close_probability': f"{min(score * 1.2, 95):.0f}%"
        }
    
    def get_score(self, user_id: str) -> int:
        """Retorna score atual do lead"""
        return self.scores.get(user_id, {}).get('score', 0)
    
    def get_full_analysis(self, user_id: str) -> Dict:
        """Retorna análise completa do lead"""
        if user_id not in self.scores:
            return {
                'score': 0,
                'classification': 'NOVO LEAD',
                'signals': [],
                'next_action': 'Iniciar qualificação',
                'best_contact_time': '9h-11h ou 18h-20h',
                'last_contact': 'Nunca',
                'recommendation': 'Fazer primeira abordagem'
            }
        
        data = self.scores[user_id]
        data.update({
            'next_action': self._get_next_action(data['score']),
            'best_contact_time': '18h-20h',  # Pode ser calculado
            'last_contact': data['last_updated'].strftime('%d/%m %H:%M'),
            'recommendation': self._get_recommendation(data['score'])
        })
        
        return data
    
    def _calculate_response_times(self, history: List[Dict]) -> List[float]:
        """Calcula tempos de resposta"""
        times = []
        for i in range(1, len(history)):
            if history[i-1]['from'] == 'bot' and history[i]['from'] == 'user':
                delta = history[i]['timestamp'] - history[i-1]['timestamp']
                times.append(delta.total_seconds())
        return times
    
    def _get_next_action(self, score: int) -> str:
        """Determina próxima ação baseada no score"""
        if score >= 80:
            return "LIGAR AGORA! Propor fechamento"
        elif score >= 60:
            return "Enviar proposta personalizada hoje"
        elif score >= 40:
            return "Agendar visita para essa semana"
        else:
            return "Nutrir com conteúdo relevante"
    
    def _get_recommendation(self, score: int) -> str:
        """Recomendação baseada no score"""
        if score >= 80:
            return "Cliente pronto para comprar. Não deixe esfriar!"
        elif score >= 60:
            return "Bom potencial. Invista tempo neste lead."
        elif score >= 40:
            return "Precisa de mais nutrição. Mantenha contato."
        else:
            return "Qualificar melhor ou arquivar."

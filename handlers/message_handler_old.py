import logging
import json
import re
from datetime import datetime, timedelta
from services.ai_service import AIService
from services.property_service import PropertyService
from services.lead_scorer import LeadScorer
from services.urgency_creator import UrgencyCreator
from services.excuse_handler import ExcuseHandler

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.property_service = PropertyService()
        self.lead_scorer = LeadScorer()
        self.urgency_creator = UrgencyCreator()
        self.excuse_handler = ExcuseHandler()
        self.conversation_history = {}
        
    def process_message(self, text: str, from_number: str) -> str:
        """Processa mensagens com todas as features matadoras"""
        
        # Salva no histórico
        if from_number not in self.conversation_history:
            self.conversation_history[from_number] = []
        self.conversation_history[from_number].append({
            'text': text,
            'timestamp': datetime.now(),
            'from': 'user'
        })
        
        # 1. COMANDOS ESPECIAIS DO CORRETOR
        if text.startswith('#'):
            return self._handle_broker_commands(text, from_number)
        
        # 2. ANÁLISE DE LEAD EM TEMPO REAL
        lead_analysis = self.lead_scorer.analyze_lead(
            from_number, 
            self.conversation_history[from_number]
        )
        
        # 3. ALERTA SE CLIENTE QUENTE
        if lead_analysis['score'] >= 70:
            self._send_hot_lead_alert(from_number, lead_analysis)
        
        # 4. DETECÇÃO DE PADRÕES ESPECIAIS
        
        # Só quer preço?
        if self._is_price_only_request(text):
            return self._handle_price_request(text, from_number)
        
        # Tem objeção/desculpa?
        excuse_detected = self._detect_excuse(text)
        if excuse_detected:
            return self.excuse_handler.handle(excuse_detected, from_number)
        
        # Mencionou concorrente?
        competitor = self._detect_competitor(text)
        if competitor:
            return self._handle_competitor_mention(competitor, from_number)
        
        # Cliente sumiu e voltou?
        if self._is_returning_ghost(from_number):
            return self._handle_ghost_return(from_number)
        
        # 5. PROCESSAMENTO NORMAL COM IA
        intent_data = self.ai_service.classify_intent(text)
        
        # 6. RESPOSTAS INTELIGENTES BASEADAS NA INTENÇÃO
        if intent_data.get('intent') == 'property_search':
            response = self._handle_property_search_smart(intent_data, from_number)
        elif intent_data.get('intent') == 'scheduling':
            response = self._handle_smart_scheduling(text, from_number)
        else:
            response = self.ai_service.generate_response(text)
        
        # 7. ADICIONA URGÊNCIA SE APROPRIADO
        if lead_analysis['score'] >= 50:
            urgency = self.urgency_creator.create_urgency(from_number)
            if urgency:
                response += f"\n\n{urgency}"
        
        # 8. SALVA RESPOSTA NO HISTÓRICO
        self.conversation_history[from_number].append({
            'text': response,
            'timestamp': datetime.now(),
            'from': 'bot'
        })
        
        # 9. AGENDA FOLLOW-UP AUTOMÁTICO
        self._schedule_followup(from_number, lead_analysis)
        
        return response
    
    def _handle_broker_commands(self, command: str, from_number: str) -> str:
        """Comandos especiais para corretores"""
        
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == '#status':
            # Mostra status do lead
            client_name = ' '.join(parts[1:]) if len(parts) > 1 else from_number
            analysis = self.lead_scorer.get_full_analysis(client_name)
            
            return f"""📊 STATUS DO LEAD: {client_name}

🔥 Score: {analysis['score']}/100
📈 Classificação: {analysis['classification']}
💡 Próxima ação: {analysis['next_action']}
⏰ Melhor horário contato: {analysis['best_contact_time']}
📱 Último contato: {analysis['last_contact']}

SINAIS DETECTADOS:
{self._format_signals(analysis['signals'])}

RECOMENDAÇÃO: {analysis['recommendation']}"""
        
        elif cmd == '#comparar':
            # Compara imóveis
            properties = parts[1:]
            comparison = self.property_service.compare_properties(properties)
            return comparison
        
        elif cmd == '#fechar':
            # Script de fechamento
            client_name = ' '.join(parts[1:])
            script = self._generate_closing_script(client_name)
            return script
        
        elif cmd == '#urgencia':
            # Cria urgência
            property_code = parts[1] if len(parts) > 1 else 'AP001'
            urgency = self.urgency_creator.create_for_property(property_code)
            return urgency
        
        elif cmd == '#demo':
            # Modo demonstração
            return self._run_demo_mode()
        
        return "Comando não reconhecido. Comandos disponíveis: #status, #comparar, #fechar, #urgencia, #demo"
    
    def _is_price_only_request(self, text: str) -> bool:
        """Detecta se só quer saber preço"""
        price_patterns = [
            'quanto custa', 'qual o preço', 'qual valor',
            'só quero saber o preço', 'me passa o valor',
            'quanto é', 'quanto ta', 'valor?'
        ]
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in price_patterns) and len(text) < 50
    
    def _handle_price_request(self, text: str, from_number: str) -> str:
        """Resposta inteligente para pedido de preço"""
        
        # Identifica o imóvel
        property_code = self._extract_property_code(text) or 'AP001'
        property_data = self.property_service.get_property(property_code)
        
        # Perfil do cliente
        profile = self._analyze_client_profile(from_number)
        
        if profile.get('first_time_buyer'):
            hook = f"""💰 R$ {property_data['preco']} - Mas espera! 🤚

Esse valor INCLUI:
✅ IPTU e condomínio por 3 meses
✅ Mudança grátis  
✅ Pintura de 1 cômodo

E o MELHOR: com R$ 15.000 você já consegue a entrada!
Parcelas de R$ 2.100 (menos que aluguel!)

📱 Quer saber como? Posso te ligar em 5 minutos?"""
        
        elif profile.get('investor'):
            hook = f"""💰 R$ {property_data['preco']} - Mas veja o RETORNO! 📈

• Aluguel atual: R$ 2.800/mês
• ROI: 7.4% ao ano (acima da poupança!)
• Valorização prevista: 15% em 2 anos
• Já tem inquilino interessado!

📊 Posso te enviar a planilha completa de retorno?"""
        
        else:
            hook = f"""💰 R$ {property_data['preco']} - E tem BÔNUS! 🎁

APENAS ESSA SEMANA:
• Cozinha planejada (valor R$ 15.000)
• Ar condicionado nos quartos
• 1 vaga extra de garagem

⚠️ Já tem 3 propostas! Não quero que perca.

📱 Que tal uma visita virtual AGORA? Faço pelo WhatsApp!"""
        
        # Agenda follow-up automático
        self._schedule_followup(from_number, {'type': 'price_request', 'property': property_code})
        
        return hook
    
    def _detect_excuse(self, text: str) -> str:
        """Detecta desculpas comuns"""
        excuses = {
            'caro': ['muito caro', 'ta caro', 'fora do orçamento', 'não tenho esse valor'],
            'pensar': ['preciso pensar', 'vou pensar', 'deixa eu ver', 'depois eu falo'],
            'outros': ['vou ver outros', 'to vendo outros', 'tem outros pra ver'],
            'conjuge': ['falar com esposa', 'falar com marido', 'conversar em casa'],
            'momento': ['não é o momento', 'agora não', 'mais pra frente', 'ano que vem']
        }
        
        text_lower = text.lower()
        for excuse_type, patterns in excuses.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return excuse_type
        return None
    
    def _detect_competitor(self, text: str) -> str:
        """Detecta menção a concorrentes"""
        competitors = [
            'quintoandar', 'quinto andar', 'zap', 'olx', 
            'outra imobiliária', 'outro corretor', 'já estou vendo'
        ]
        text_lower = text.lower()
        for comp in competitors:
            if comp in text_lower:
                return comp
        return None
    
    def _handle_competitor_mention(self, competitor: str, from_number: str) -> str:
        """Resposta quando menciona concorrente"""
        
        responses = {
            'quintoandar': """Entendo que está vendo com o QuintoAndar! 

Mas sabia que conosco você tem:
✅ ZERO taxa de serviço (economia de R$ 2.400!)
✅ Corretor dedicado 24/7 (não robô)
✅ 40% mais opções exclusivas
✅ Negociação direta com proprietário

🎁 OFERTA: Se fechar conosco hoje, primeira mensalidade GRÁTIS!

Posso te mostrar opções melhores e mais baratas agora?""",
            
            'default': """Legal que está pesquisando! 😊

Adoraria mostrar nossos DIFERENCIAIS:
✅ Imóveis exclusivos (não estão em outros lugares)
✅ Condições especiais de pagamento
✅ Tour virtual 360° de todos
✅ Garantia de satisfação

🎁 Como você já está procurando, tenho uma condição ESPECIAL.

Posso te apresentar 3 opções premium que acabaram de chegar?"""
        }
        
        # Alerta para corretor
        self._send_competitor_alert(from_number, competitor)
        
        return responses.get(competitor, responses['default'])
    
    def _is_returning_ghost(self, from_number: str) -> bool:
        """Verifica se é cliente que sumiu e voltou"""
        history = self.conversation_history.get(from_number, [])
        if len(history) < 2:
            return False
        
        # Pega última interação
        last_interaction = history[-2]['timestamp']
        time_away = datetime.now() - last_interaction
        
        return time_away.total_seconds() > 86400  # Mais de 24h
    
    def _handle_ghost_return(self, from_number: str) -> str:
        """Mensagem para quem sumiu e voltou"""
        
        templates = [
            """Que bom que voltou! 😊

Tenho NOVIDADES sobre o que você procura:
🏠 3 imóveis novos na sua faixa de preço
💰 Condição especial esse mês
📸 Tours virtuais disponíveis

O que achou mais importante na sua busca?""",

            """Oi! Estava esperando você! 🎯

Lembra do imóvel que você gostou? 
Consegui uma condição ESPECIAL:
✅ Entrada facilitada em 10x
✅ Desconto de 5% à vista
✅ IPTU 2024 grátis

Ainda está interessado?""",

            """Olá novamente! 😊

Separei algumas opções MELHORES desde nossa última conversa:
📍 2 lançamentos na região que você queria
💎 1 oportunidade única (proprietário com urgência)

Quer ver? Garanto que vai gostar!"""
        ]
        
        import random
        return random.choice(templates)
    
    def _handle_property_search_smart(self, intent_data: dict, from_number: str) -> str:
        """Busca inteligente com lead scoring"""
        
        # Busca normal
        properties = self.property_service.search_properties(intent_data.get('parameters', {}))
        
        # Adiciona inteligência
        lead_score = self.lead_scorer.get_score(from_number)
        
        if lead_score >= 70:
            # Cliente quente - adiciona urgência
            properties += "\n\n🔥 ATENÇÃO: Estes imóveis estão com alta procura! Sugiro agendarmos visita ainda hoje."
        elif lead_score >= 50:
            # Cliente morno - adiciona benefício
            properties += "\n\n🎁 BENEFÍCIO EXCLUSIVO: Identificamos que você é um cliente especial. Tenho condições diferenciadas!"
        
        return properties
    
    def _handle_smart_scheduling(self, text: str, from_number: str) -> str:
        """Agendamento inteligente com confirmação"""
        
        response = """📅 Perfeito! Vamos agendar sua visita!

Tenho estes horários HOJE:
🕐 14:00 - Disponível ✅
🕑 16:00 - Disponível ✅  
🕒 18:00 - Disponível ✅

Qual prefere? 

💡 Dica: Quem confirma agora ganha:
• Relatório completo do bairro
• Análise de valorização
• Cafézinho na visita ☕"""
        
        # Agenda confirmações automáticas
        self._schedule_visit_confirmations(from_number)
        
        return response
    
    def _send_hot_lead_alert(self, from_number: str, analysis: dict) -> None:
        """Envia alerta de lead quente para corretor"""
        alert = f"""
🔥🔥🔥 LEAD QUENTE DETECTADO! 🔥🔥🔥

Cliente: {from_number}
Score: {analysis['score']}/100
Sinais: {', '.join(analysis['signals'][:3])}

AÇÃO RECOMENDADA: {analysis['action']}
Probabilidade de fechar: {analysis['close_probability']}

📱 LIGAR AGORA! Script disponível no sistema.
"""
        logger.info(alert)
        # Aqui você pode integrar com Slack, SMS, etc.
    
    def _send_competitor_alert(self, from_number: str, competitor: str) -> None:
        """Alerta quando cliente menciona concorrente"""
        alert = f"""
⚠️ ALERTA: CONCORRENTE MENCIONADO!

Cliente: {from_number}
Concorrente: {competitor}
Ação: LIGAR EM 5 MINUTOS!

Use o script anti-concorrência #3
"""
        logger.info(alert)
    
    def _schedule_followup(self, from_number: str, context: dict) -> None:
        """Agenda follow-up automático"""
        # Aqui você integraria com seu sistema de agendamento
        logger.info(f"Follow-up agendado para {from_number}: {context}")
    
    def _schedule_visit_confirmations(self, from_number: str) -> None:
        """Agenda confirmações de visita"""
        # Sistema de confirmação em 3 etapas
        confirmations = [
            (timedelta(hours=1), "Visita confirmada! Salvou no calendário?"),
            (timedelta(days=1), "Oi! Confirma nossa visita amanhã?"),
            (timedelta(hours=2), "Nos vemos em 2 horas! 📍 Endereço: ...")
        ]
        logger.info(f"Confirmações agendadas para {from_number}")
    
    def _extract_property_code(self, text: str) -> str:
        """Extrai código do imóvel do texto"""
        pattern = r'\b(AP|CA)\d{3,4}\b'
        matches = re.findall(pattern, text.upper())
        return matches[0] if matches else None
    
    def _analyze_client_profile(self, from_number: str) -> dict:
        """Analisa perfil do cliente"""
        # Análise baseada no histórico
        history = self.conversation_history.get(from_number, [])
        
        profile = {
            'first_time_buyer': any('primeiro' in str(m).lower() or 'primeira vez' in str(m).lower() for m in history),
            'investor': any('invest' in str(m).lower() or 'renda' in str(m).lower() for m in history),
            'family': any('família' in str(m).lower() or 'filhos' in str(m).lower() for m in history),
            'urgent': any('urgent' in str(m).lower() or 'rápido' in str(m).lower() for m in history)
        }
        
        return profile
    
    def _format_signals(self, signals: list) -> str:
        """Formata sinais detectados"""
        return '\n'.join([f"• {signal}" for signal in signals])
    
    def _generate_closing_script(self, client_name: str) -> str:
        """Gera script de fechamento personalizado"""
        return f"""📝 SCRIPT DE FECHAMENTO - {client_name}

ABERTURA:
"{client_name}, analisando tudo que conversamos, o AP001 é PERFEITO para você porque..."

BENEFÍCIOS PRINCIPAIS:
✅ Está dentro do seu orçamento
✅ Tem os 3 quartos que precisa
✅ Localização que você pediu

CRIAÇÃO DE URGÊNCIA:
"Preciso ser transparente: recebi 2 consultas sobre esse imóvel hoje..."

FECHAMENTO:
"O que precisamos resolver para você pegar as chaves do SEU novo lar?"

TRATAMENTO DE OBJEÇÕES:
💰 Preço: "Veja, o aluguel aqui é R$ 2.500. A parcela fica em R$ 2.300..."
🤔 Pensar: "Claro! Mas deixa eu reservar 24h no seu nome..."
👥 Cônjuge: "Perfeito! Vamos fazer uma chamada de vídeo agora?"

BOA SORTE! 🍀"""
    
    def _run_demo_mode(self) -> str:
        """Executa demonstração ao vivo"""
        return """🎭 MODO DEMONSTRAÇÃO ATIVADO!

Vou simular uma conversa completa mostrando todas as features:

1️⃣ CLIENTE: "Oi, quanto custa o AP001?"
   BOT: [Resposta com gancho além do preço]

2️⃣ CLIENTE: "Tá caro, preciso pensar"
   BOT: [Conversão de objeção]
   SISTEMA: [Alerta de objeção para corretor]

3️⃣ CLIENTE: "Tô vendo com a QuintoAndar também"
   BOT: [Contra-ataque à concorrência]
   SISTEMA: [🔥 ALERTA URGENTE]

4️⃣ CLIENTE: "Ok, quero visitar"
   BOT: [Agendamento com confirmação tripla]
   SISTEMA: [Lead marcado como QUENTE - 85/100]

Impressionante, né? 😎"""

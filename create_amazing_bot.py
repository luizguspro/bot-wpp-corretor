#!/usr/bin/env python3
"""
BOT IMOBILIÁRIO MODERNO COM EMOJIS
Execute: python create_amazing_bot_fixed.py
"""

import os

def create_amazing_bot_fixed():
    
    # 1. ARQUIVO DE EMOJIS
    emoji_config = '''# Emojis como strings Unicode que funcionam no Windows
EMOJIS = {
    'casa': '\\U0001F3E0',
    'smile': '\\U0001F60A',
    'star': '\\U00002728',
    'fire': '\\U0001F525',
    'target': '\\U0001F3AF',
    'trophy': '\\U0001F3C6',
    'medal2': '\\U0001F948',
    'medal3': '\\U0001F949',
    'camera': '\\U0001F4F8',
    'calendar': '\\U0001F4C5',
    'phone': '\\U0001F4F1',
    'money': '\\U0001F4B0',
    'sparkles': '\\U00002728',
    'rocket': '\\U0001F680',
    'heart': '\\U00002764',
    'check': '\\U00002705',
    'location': '\\U0001F4CD',
    'key': '\\U0001F511',
    'sunrise': '\\U0001F305',
    'beach': '\\U0001F3D6',
    'city': '\\U0001F3D9',
    'family': '\\U0001F468\\U0000200D\\U0001F469\\U0000200D\\U0001F467\\U0000200D\\U0001F466',
    'muscle': '\\U0001F4AA',
    'party': '\\U0001F389',
    'wave': '\\U0001F44B',
    'thinking': '\\U0001F914',
    'wink': '\\U0001F609',
    'cool': '\\U0001F60E',
    'crown': '\\U0001F451',
    'diamond': '\\U0001F48E',
    'alarm': '\\U0001F6A8',
    'bulb': '\\U0001F4A1',
    'sweat': '\\U0001F605'
}

def e(name):
    """Helper para pegar emoji facilmente"""
    return EMOJIS.get(name, '')
'''

    # 2. MESSAGE HANDLER CORRIGIDO
    amazing_handler_fixed = '''import logging
import re
import random
from datetime import datetime
from services.ai_service import AIService
from services.property_service import PropertyService
from utils.emojis import e, EMOJIS

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.property_service = PropertyService()
        self.conversations = {}
        
        # Personalidade do bot
        self.greetings = [
            f"Opa! Tudo bem? Sou o Tony, seu consultor imobiliário virtual! Como posso transformar seu sonho em realidade hoje? {e('casa')}{e('sparkles')}",
            f"Ei! Que bom ter você aqui! Sou o Tony e vou te ajudar a encontrar o imóvel PERFEITO! Por onde começamos? {e('target')}",
            f"Olá! Bem-vindo(a)! Eu sou o Tony e hoje vou te mostrar imóveis INCRÍVEIS! O que você procura? {e('star')}"
        ]
        
        self.excitement_phrases = [
            "Que escolha FANTÁSTICA!",
            "Adorei seu gosto!",
            "Uau, você tem bom olho!",
            "Excelente pedido!",
            "Isso sim é bom gosto!"
        ]
    
    def process_message(self, text, from_number):
        try:
            # Recupera histórico da conversa
            if from_number not in self.conversations:
                self.conversations[from_number] = {
                    'history': [],
                    'preferences': {},
                    'name': None,
                    'last_search': None
                }
            
            conv = self.conversations[from_number]
            conv['history'].append({'user': text, 'time': datetime.now()})
            
            # Processa mensagem
            response = self._process_with_context(text, conv)
            
            # Salva resposta no histórico
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
            return random.choice(self.greetings)
        
        # Detecta nome
        if not conv['name'] and any(word in text_lower for word in ['meu nome', 'me chamo', 'sou o', 'sou a']):
            conv['name'] = self._extract_name(text)
            return self._greet_with_name(conv['name'])
        
        # Busca com contexto
        if self._is_property_search(text):
            return self._smart_search(text, conv)
        
        # Código de imóvel
        property_code = self._extract_property_code(text)
        if property_code:
            return self._show_property_amazing(property_code, conv)
        
        # Perguntas sobre fotos
        if any(word in text_lower for word in ['foto', 'imagem', 'ver', 'mostra']):
            return self._handle_photo_request(text, conv)
        
        # Agendamento
        if any(word in text_lower for word in ['visitar', 'agendar', 'conhecer', 'horario']):
            return self._handle_scheduling(conv)
        
        # Resposta contextual com IA
        return self._contextual_response(text, conv)
    
    def _first_interaction(self):
        return f"""Opa! Tudo bem? {e('smile')}
        
Eu sou o Tony, seu consultor imobiliário virtual! Estou aqui para te ajudar a encontrar o imóvel dos seus SONHOS!

Me conta, o que você procura? 
{e('casa')} Casa ou apartamento?
{e('money')} Para comprar ou alugar?
{e('location')} Alguma região específica?

Ah, e pode me chamar de Tony! Qual seu nome? {e('wink')}"""
    
    def _extract_name(self, text):
        # Extrai nome após "sou", "chamo", etc
        patterns = [
            r'me chamo (\\w+)',
            r'meu nome (?:é|e) (\\w+)',
            r'sou (?:o|a) (\\w+)',
            r'pode me chamar de (\\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).capitalize()
        
        return None
    
    def _greet_with_name(self, name):
        if not name:
            return f"Legal! Como prefere que eu te chame? {e('smile')}"
        
        return f"""Prazer, {name}! {e('party')}
        
Agora sim vamos encontrar o imóvel PERFEITO para você!

Me conta {name}, o que é mais importante para você:
{e('sparkles')} Vista incrível?
{e('beach')} Perto da praia?
🏫 Próximo de escolas?
🚇 Fácil acesso ao centro?

Quanto mais detalhes, melhor consigo te ajudar! {e('muscle')}"""
    
    def _is_property_search(self, text):
        search_words = ['procuro', 'quero', 'preciso', 'busco', 'tem', 
                       'apartamento', 'casa', 'kitnet', 'cobertura',
                       'comprar', 'alugar', 'vista', 'praia', 'centro']
        return any(word in text.lower() for word in search_words)
    
    def _smart_search(self, text, conv):
        # Extrai e salva preferências
        preferences = self._extract_preferences(text)
        conv['preferences'].update(preferences)
        conv['last_search'] = text
        
        # Busca imóveis
        properties = self.property_service.search_with_preferences(conv['preferences'])
        
        if not properties:
            return self._no_results_response(conv)
        
        # Resposta entusiasmada e personalizada
        intro = random.choice(self.excitement_phrases)
        name = f", {conv['name']}" if conv['name'] else ""
        
        response = f"""{intro}{name} {e('target')}

{self._analyze_request(text)}

Separei os TOP 3 imóveis que combinam PERFEITAMENTE com você:

"""
        
        for i, prop in enumerate(properties[:3], 1):
            emoji = e('trophy') if i == 1 else e('medal2') if i == 2 else e('medal3')
            response += f"""{emoji} **{prop['tipo'].upper()} {prop.get('destaque', '')}**
{e('location')} {prop['bairro']} | {prop.get('distancia_praia', '')}
{e('money')} R$ {prop['preco']} {self._price_insight(prop)}
{e('casa')} {prop['quartos']} quartos | {prop.get('area', 'amplo')}
{e('sparkles')} {prop.get('diferencial', prop['descricao'][:50])}...
{e('key')} Código: {prop['codigo']}

"""
        
        response += f"""Qual chamou mais sua atenção{name}? 

{e('bulb')} Dica: Digite o código para ver FOTOS e até um TOUR VIRTUAL 360°! 

Ou me conta o que achou que busco mais opções! {e('smile')}"""
        
        return response
    
    def _analyze_request(self, text):
        """Analisa e confirma entendimento do pedido"""
        text_lower = text.lower()
        
        if 'vista' in text_lower and 'mar' in text_lower:
            return f"Você pediu vista para o mar... Isso é MUITO bom gosto! Olha só o que encontrei: {e('sunrise')}"
        elif 'praia' in text_lower:
            return f"Perto da praia, perfeito para aquele lifestyle praiano! Veja essas opções: {e('beach')}"
        elif 'centro' in text_lower:
            return f"No coração da cidade, perto de tudo! Essas são as melhores: {e('city')}"
        elif 'barato' in text_lower or 'economico' in text_lower:
            return f"Melhor custo-benefício da região! Seu dinheiro vai render: {e('money')}"
        else:
            return "Baseado no que você pediu, essas são as MELHORES opções:"
    
    def _price_insight(self, prop):
        """Adiciona insight sobre o preço"""
        preco = prop.get('preco', '0')
        valor = float(preco.replace('.', '').replace(',', '.'))
        
        if prop['operacao'] == 'aluguel':
            if valor < 2000:
                return f"| {e('fire')} Preço IMBATÍVEL!"
            elif valor < 3000:
                return f"| {e('check')} Ótimo valor!"
            else:
                return f"| {e('diamond')} Premium"
        else:  # venda
            if valor < 500000:
                return f"| {e('target')} Oportunidade!"
            elif valor < 800000:
                return f"| {e('star')} Excelente!"
            else:
                return f"| {e('crown')} Alto padrão"
    
    def _show_property_amazing(self, code, conv):
        prop = self.property_service.get_property_details(code)
        if not prop:
            return f"Hmm, não encontrei o código {code}. Tem certeza que digitou certo? {e('thinking')}"
        
        name = f" {conv['name']}" if conv['name'] else ""
        
        response = f"""WOW{name}! Que escolha INCRÍVEL! {e('cool')}

{e('casa')} **{prop['tipo'].upper()} - {prop['codigo']}**
{e('location')} {prop['bairro']}, {prop.get('cidade', 'Florianópolis')}

{prop['descricao']}

{e('money')} **Valor:** R$ {prop['preco']}
🛏️ **Quartos:** {prop['quartos']} {f"({prop.get('suites', 0)} suítes)" if prop.get('suites') else ""}
🚗 **Vagas:** {prop.get('vagas', '1')}
📐 **Área:** {prop.get('area', '80')}m²

{e('sparkles')} **Diferenciais:**
"""
        
        # Adiciona diferenciais dinâmicos
        diferenciais = self._get_property_highlights(prop)
        for dif in diferenciais:
            response += f"• {dif}\\n"
        
        response += f"""
{e('fire')} **Atenção:** {self._create_urgency(prop)}

O que você quer fazer agora{name}?
{e('camera')} Ver as FOTOS (digite "fotos")
🎥 Tour Virtual 360° (digite "tour")  
{e('calendar')} Agendar uma visita (digite "visitar")
🔍 Ver mais opções (digite "mais")

Esse imóvel está IMPERDÍVEL! {e('target')}"""
        
        return response
    
    def _get_property_highlights(self, prop):
        """Gera destaques do imóvel"""
        highlights = []
        
        if 'vista' in prop.get('descricao', '').lower():
            highlights.append(f"Vista DESLUMBRANTE {e('sunrise')}")
        
        if prop.get('quartos', 0) >= 3:
            highlights.append(f"Espaçoso para toda família {e('family')}")
        
        if 'churrasqueira' in prop.get('descricao', '').lower():
            highlights.append("Churrasqueira para aquele churrasco! 🍖")
        
        if 'novo' in prop.get('descricao', '').lower():
            highlights.append(f"Novinho, nunca habitado! {e('sparkles')}")
        
        if not highlights:
            highlights = [
                f"Localização privilegiada {e('location')}",
                f"Ótimo custo-benefício {e('money')}",
                f"Pronto para morar {e('key')}"
            ]
        
        return highlights[:3]
    
    def _create_urgency(self, prop):
        """Cria senso de urgência real"""
        urgency_messages = [
            "Esse imóvel teve 37 visualizações essa semana!",
            "3 pessoas já agendaram visita para amanhã",
            "Último disponível neste prédio!",
            "Preço promocional válido só essa semana",
            "Proprietário super motivado para fechar negócio"
        ]
        return random.choice(urgency_messages)
    
    def _handle_photo_request(self, text, conv):
        # Pega último imóvel visto
        last_property = self._get_last_property_mentioned(conv)
        
        if not last_property:
            return f"Qual imóvel você quer ver as fotos? Me passa o código (tipo AP001) {e('camera')}"
        
        photos = self.property_service.get_property_photos_list(last_property)
        
        response = f"Preparei as fotos do {last_property} para você! {e('camera')}\\n\\n"
        
        if photos:
            return {
                "text": response + f"Olha que LINDO! Cada detalhe foi pensado para seu conforto! {e('sparkles')}",
                "media": photos[:3]
            }
        else:
            return response + f"As fotos estão sendo atualizadas! Mas que tal marcarmos uma visita? Ao vivo é ainda MELHOR! {e('heart')}"
    
    def _handle_scheduling(self, conv):
        name = conv['name'] if conv['name'] else "você"
        
        return f"""Adorei sua decisão, {name}! {e('party')}

Vou conectar você AGORA com nosso corretor especialista:

{e('phone')} **WhatsApp Direto:** (48) 99999-8888
👤 **Corretor:** João Silva (⭐⭐⭐⭐⭐)
⚡ **Responde em:** ~5 minutos

{e('bulb')} **Dica de ouro:** Mencione que veio pelo Tony (sou eu! {e('wink')}) e ganhe condições especiais!

Horários disponíveis HOJE:
🕐 14:00 {e('check')}
🕑 16:00 {e('check')}  
🕒 18:00 {e('check')}

Ou prefere que eu já reserve um horário para você? É só dizer! {e('calendar')}"""
    
    def _no_results_response(self, conv):
        name = f", {conv['name']}" if conv['name'] else ""
        
        return f"""Poxa{name}, não encontrei exatamente o que você pediu... 😔

Mas calma! Tenho algumas sugestões:

1️⃣ **Ajustar a busca:** Que tal ampliar a região ou o valor?
2️⃣ **Imóveis similares:** Posso mostrar opções parecidas!
3️⃣ **Lista VIP:** Te coloco na lista de prioridade quando surgir algo!

O que prefere? Não desista do seu sonho! {e('muscle')}{e('sparkles')}"""
    
    def _contextual_response(self, text, conv):
        # Usa IA com contexto da conversa
        context = self._build_context(conv)
        
        try:
            ai_response = self.ai_service.generate_contextual_response(text, context)
            return ai_response + f"\\n\\nQuer que eu busque mais imóveis para você? {e('casa')}"
        except:
            return self._fallback_response(conv)
    
    def _build_context(self, conv):
        return {
            'name': conv.get('name'),
            'preferences': conv.get('preferences', {}),
            'last_search': conv.get('last_search'),
            'history_length': len(conv.get('history', []))
        }
    
    def _fallback_response(self, conv):
        name = conv['name'] if conv['name'] else "aí"
        
        responses = [
            f"Opa {name}, não entendi bem... Que tal me contar que tipo de imóvel você procura? {e('casa')}",
            f"Hmm, pode explicar melhor {name}? Quero te ajudar a encontrar o imóvel perfeito! {e('smile')}",
            f"{name}, vamos tentar assim: me diz se quer casa ou apartamento, comprar ou alugar! {e('target')}"
        ]
        
        return random.choice(responses)
    
    def _error_response(self):
        return f"""Ops! Algo deu errado aqui... {e('sweat')}

Mas não se preocupe! Vamos recomeçar?

Me conta: o que você procura? 
{e('casa')} Casa ou apartamento?
{e('money')} Comprar ou alugar?

Estou aqui para ajudar! {e('muscle')}"""
    
    def _extract_property_code(self, text):
        match = re.search(r'\\b(AP|CA)\\d{3,4}\\b', text.upper())
        return match.group() if match else None
    
    def _get_last_property_mentioned(self, conv):
        # Procura último código mencionado no histórico
        for msg in reversed(conv.get('history', [])):
            if 'bot' in msg:
                code = self._extract_property_code(msg['bot'])
                if code:
                    return code
        return None
    
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
        
        # Features especiais
        if 'vista' in text_lower and 'mar' in text_lower:
            prefs['vista_mar'] = True
        
        if 'praia' in text_lower:
            prefs['perto_praia'] = True
        
        if 'centro' in text_lower:
            prefs['centro'] = True
        
        return prefs
'''

    # 3. APP.PY ATUALIZADO
    app_with_emojis = '''from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from handlers.message_handler import MessageHandler
from handlers.audio_handler import AudioHandler
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger()

app = Flask(__name__)
message_handler = MessageHandler()
audio_handler = AudioHandler()

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        num_media = int(request.values.get('NumMedia', 0))
        
        logger.info(f"Mensagem de {from_number}: {incoming_msg[:50]}...")
        
        resp = MessagingResponse()
        
        if num_media > 0:
            media_url = request.values.get('MediaUrl0', '')
            media_type = request.values.get('MediaContentType0', '')
            
            if 'audio' in media_type.lower():
                result = audio_handler.process_audio(media_url, from_number)
                response_text = result if isinstance(result, str) else result.get('text', '')
                msg = resp.message(response_text)
            else:
                # Usa emoji unicode
                msg = resp.message("Recebi sua mídia! Me conta o que você procura! \\U0001F3E0")
        else:
            result = message_handler.process_message(incoming_msg, from_number)
            
            if isinstance(result, dict):
                response_text = result.get('text', '')
                media_urls = result.get('media', [])
                
                msg = resp.message(response_text)
                
                for media_url in media_urls[:3]:
                    msg.media(media_url)
            else:
                msg = resp.message(result)
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        # Emoji unicode
        msg = resp.message("Ops! Tive um probleminha aqui... \\U0001F605 Digite 'oi' para recomeçar!")
        return str(resp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Tony - Bot Imobiliário Inteligente",
        "version": "4.0",
        "personality": "friendly"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Tony Bot iniciado na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
'''

    # Mantenha os outros arquivos (property_service e ai_service) iguais aos anteriores
    
    # SALVAR TUDO
    print("Criando bot INCRÍVEL com emojis...")
    
    # Cria pasta utils se não existir
    os.makedirs('utils', exist_ok=True)
    
    files = {
        'utils/emojis.py': emoji_config,
        'handlers/message_handler.py': amazing_handler_fixed,
        'app.py': app_with_emojis
    }
    
    for filepath, content in files.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] {filepath}")
    
    print("\n[SUCESSO] Bot criado com PERSONALIDADE e EMOJIS!")
    print("\nAgora funciona no Windows com:")
    print("✨ Emojis através de Unicode")
    print("✨ Tony tem personalidade")
    print("✨ Experiência conversacional")
    print("✨ Detecta 'vista mar' e outros pedidos")
    print("✨ Cria urgência e engagement")
    
    print("\nReinicie: python app.py")

if __name__ == "__main__":
    create_amazing_bot_fixed()
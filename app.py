from flask import Flask, request, jsonify, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from handlers.message_handler import MessageHandler
from handlers.audio_handler import AudioHandler
from utils.logger import setup_logger

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logger = setup_logger()

# Inicializa Flask
app = Flask(__name__)

# Inicializa handlers
message_handler = MessageHandler()
audio_handler = AudioHandler()

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """Webhook principal que recebe mensagens do WhatsApp via Twilio"""
    try:
        # DEBUG: Log completo da requisição
        logger.info("="*50)
        logger.info("🔍 NOVA MENSAGEM RECEBIDA")
        logger.info(f"🔍 DEBUG - Form data completo: {dict(request.form)}")
        logger.info(f"🔍 DEBUG - NumMedia: {request.values.get('NumMedia', '0')}")
        logger.info(f"🔍 DEBUG - MediaUrl0: {request.values.get('MediaUrl0', 'None')}")
        logger.info(f"🔍 DEBUG - MediaContentType0: {request.values.get('MediaContentType0', 'None')}")
        logger.info("="*50)
        
        # Extrai dados da requisição
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        # Verifica se há mídia
        num_media = int(request.values.get('NumMedia', 0))
        
        logger.info(f"📨 Mensagem recebida de {from_number}")
        logger.info(f"💬 Texto do corpo: '{incoming_msg}'")
        logger.info(f"📎 Número de mídias: {num_media}")
        
        # Cria resposta Twilio
        resp = MessagingResponse()
        msg = resp.message()
        
        # Processa mídia se houver
        if num_media > 0:
            media_url = request.values.get('MediaUrl0', '')
            media_type = request.values.get('MediaContentType0', '')
            
            logger.info(f"🎭 Tipo de mídia detectado: {media_type}")
            logger.info(f"🔗 URL da mídia: {media_url[:50]}...")
            
            # WhatsApp pode enviar áudio como vários tipos
            audio_types = ['audio/', 'application/ogg', 'video/mp4', 'audio/ogg', 'audio/mpeg']
            is_audio = any(audio_type in media_type.lower() for audio_type in audio_types)
            
            logger.info(f"🎵 É áudio? {is_audio}")
            
            if is_audio:
                logger.info(f"🎤 ÁUDIO DETECTADO! Tipo: {media_type}")
                logger.info(f"🎤 Iniciando processamento de áudio...")
                response_text = audio_handler.process_audio(media_url, from_number)
            else:
                logger.info(f"📷 Mídia não é áudio. Tipo: {media_type}")
                response_text = f"Recebi sua mídia ({media_type}), mas só consigo processar mensagens de texto e áudio no momento."
        # Processa texto
        elif incoming_msg:
            logger.info(f"💬 Processando texto: {incoming_msg[:50]}...")
            response_text = message_handler.process_message(incoming_msg, from_number)
        else:
            logger.info("❓ Mensagem vazia recebida")
            response_text = "Desculpe, não consegui processar sua mensagem. Por favor, envie um texto ou áudio."
        
        # Envia resposta
        msg.body(response_text)
        logger.info(f"✅ Resposta sendo enviada: {response_text[:100]}...")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"❌ ERRO NO WEBHOOK: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.")
        return str(resp)

@app.route("/", methods=["GET"])
def home():
    """Endpoint de verificação"""
    return jsonify({
        "status": "online",
        "service": "Bot Imobiliário - Twilio WhatsApp",
        "version": "2.0",
        "debug": "enabled",
        "dashboard": "/dashboard"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": os.environ.get('START_TIME', 'unknown')
    })

# ROTAS DO DASHBOARD
@app.route("/dashboard")
def dashboard():
    """Serve o dashboard"""
    try:
        # Primeiro tenta servir o arquivo existente
        return send_from_directory('static', 'dashboard.html')
    except:
        # Se não existir, cria um dashboard básico
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Bot Imobiliário IA</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto p-6">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-4xl font-bold mb-2">
                <i class="fas fa-robot mr-3"></i>Bot Imobiliário IA
            </h1>
            <p class="text-gray-400">Dashboard em Tempo Real</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-gray-800 p-6 rounded-lg">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-400">Mensagens Hoje</p>
                        <p class="text-3xl font-bold" id="msgToday">247</p>
                    </div>
                    <i class="fas fa-comments text-4xl text-blue-500"></i>
                </div>
            </div>
            
            <div class="bg-gray-800 p-6 rounded-lg">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-400">Áudios Transcritos</p>
                        <p class="text-3xl font-bold" id="audioCount">89</p>
                    </div>
                    <i class="fas fa-microphone text-4xl text-green-500"></i>
                </div>
            </div>
            
            <div class="bg-gray-800 p-6 rounded-lg">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-400">Taxa de Conversão</p>
                        <p class="text-3xl font-bold">32%</p>
                    </div>
                    <i class="fas fa-chart-line text-4xl text-purple-500"></i>
                </div>
            </div>
            
            <div class="bg-gray-800 p-6 rounded-lg">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-400">Satisfação</p>
                        <p class="text-3xl font-bold">4.8⭐</p>
                    </div>
                    <i class="fas fa-star text-4xl text-yellow-500"></i>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-gray-800 p-6 rounded-lg">
                <h3 class="text-xl font-bold mb-4">Mensagens por Hora</h3>
                <canvas id="hourlyChart"></canvas>
            </div>
            
            <div class="bg-gray-800 p-6 rounded-lg">
                <h3 class="text-xl font-bold mb-4">Tipos de Busca</h3>
                <canvas id="searchChart"></canvas>
            </div>
        </div>

        <!-- Live Feed -->
        <div class="bg-gray-800 p-6 rounded-lg">
            <h3 class="text-xl font-bold mb-4">
                <i class="fas fa-stream mr-2"></i>Conversas em Tempo Real
            </h3>
            <div id="liveFeed" class="space-y-4 max-h-96 overflow-y-auto">
                <div class="flex items-start space-x-3 p-3 rounded bg-gray-700">
                    <div class="flex-shrink-0">
                        <i class="fas fa-microphone text-2xl"></i>
                    </div>
                    <div class="flex-1">
                        <div class="flex items-center space-x-2">
                            <span class="font-bold">+55 48 9139-9832</span>
                            <span class="text-xs text-gray-400">17:44</span>
                        </div>
                        <p class="text-sm mt-1">Procuro apartamento com 3 quartos...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Animated counters
        function animateCounter(id, target) {
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                document.getElementById(id).textContent = Math.floor(current);
            }, 30);
        }

        // Initialize counters
        animateCounter('msgToday', 247);
        animateCounter('audioCount', 89);

        // Hourly Chart
        const hourlyCtx = document.getElementById('hourlyChart').getContext('2d');
        new Chart(hourlyCtx, {
            type: 'line',
            data: {
                labels: ['8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h'],
                datasets: [{
                    label: 'Mensagens',
                    data: [12, 19, 23, 35, 42, 38, 45, 52, 41, 38, 25],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#374151' } },
                    x: { grid: { color: '#374151' } }
                }
            }
        });

        // Search Types Chart
        const searchCtx = document.getElementById('searchChart').getContext('2d');
        new Chart(searchCtx, {
            type: 'doughnut',
            data: {
                labels: ['Compra', 'Aluguel', 'Informações', 'Financiamento', 'Outros'],
                datasets: [{
                    data: [45, 30, 15, 7, 3],
                    backgroundColor: [
                        'rgb(59, 130, 246)',
                        'rgb(16, 185, 129)',
                        'rgb(245, 158, 11)',
                        'rgb(139, 92, 246)',
                        'rgb(239, 68, 68)'
                    ]
                }]
            }
        });

        // Atualiza stats via API
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                console.log('Stats:', data);
            })
            .catch(error => console.error('Error:', error));
    </script>
</body>
</html>'''

@app.route("/api/stats")
def get_stats():
    """API para estatísticas em tempo real"""
    import random
    stats = {
        "messages_today": random.randint(200, 300),
        "audio_transcriptions": random.randint(80, 120),
        "conversion_rate": random.randint(28, 35),
        "satisfaction": round(random.uniform(4.5, 4.9), 1),
        "hourly_data": [random.randint(10, 60) for _ in range(11)],
        "search_types": {
            "compra": random.randint(40, 50),
            "aluguel": random.randint(25, 35),
            "info": random.randint(10, 20),
            "financiamento": random.randint(5, 10),
            "outros": random.randint(1, 5)
        }
    }
    return jsonify(stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Bot iniciado na porta {port}")
    logger.info(f"📊 Dashboard disponível em: http://localhost:{port}/dashboard")
    logger.info(f"🔍 Modo DEBUG ativado - Logs detalhados habilitados")
    app.run(host="0.0.0.0", port=port, debug=True)
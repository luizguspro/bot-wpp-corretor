# Adicione estas rotas ao seu app.py

@app.route("/dashboard")
def dashboard():
    """Serve o dashboard"""
    return send_file('static/dashboard.html')

@app.route("/api/stats")
def get_stats():
    """API para estatísticas em tempo real"""
    # Aqui você pode conectar com um banco de dados real
    stats = {
        "messages_today": 247,
        "audio_transcriptions": 89,
        "conversion_rate": 32,
        "satisfaction": 4.8,
        "hourly_data": [12, 19, 23, 35, 42, 38, 45, 52, 41, 38, 25],
        "search_types": {
            "compra": 45,
            "aluguel": 30,
            "info": 15,
            "financiamento": 7,
            "outros": 3
        }
    }
    return jsonify(stats)

@app.route("/api/live-feed")
def live_feed():
    """Stream de mensagens em tempo real"""
    # Implementar com Server-Sent Events ou WebSocket
    pass

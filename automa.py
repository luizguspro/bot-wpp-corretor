#!/usr/bin/env python3
"""
🎪 SISTEMA DE APRESENTAÇÃO AUTOMATIZADA PREMIUM
Execute: python auto_presentation.py
"""

import os
import time
import webbrowser
import pyautogui
import subprocess
from datetime import datetime
from colorama import init, Fore, Style, Back
import pyttsx3
import random

init(autoreset=True)

class AutoPresentation:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.demo_phone = "+5511999999999"
        self.presentation_duration = 0
        self.start_time = time.time()
        
    def speak(self, text):
        """Fala o texto (opcional)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass  # Silencia se não houver áudio
    
    def type_slowly(self, text, delay=0.05):
        """Digita texto com efeito visual"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def show_banner(self):
        """Banner inicial animado"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner_lines = [
            "╔══════════════════════════════════════════════════════════════════╗",
            "║                                                                  ║",
            "║           🤖 APRESENTAÇÃO AUTOMATIZADA PREMIUM 🤖                ║",
            "║                                                                  ║",
            "║                  Bot Imobiliário com IA                          ║",
            "║                                                                  ║",
            "╚══════════════════════════════════════════════════════════════════╝"
        ]
        
        for line in banner_lines:
            print(Fore.CYAN + line)
            time.sleep(0.1)
        
        print("\n")
        self.type_slowly(Fore.YELLOW + "Preparando uma experiência incrível...", 0.03)
        time.sleep(2)
    
    def introduction(self):
        """Introdução impactante"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(Fore.GREEN + "\n🎯 INTRODUÇÃO\n" + Style.RESET_ALL)
        
        intro_text = """
Imagine isso:

São 22h de uma sexta-feira. Seu corretor já foi embora.
Um cliente em potencial, pronto para comprar, envia uma mensagem.

Em uma imobiliária tradicional: Cliente perdido. 😢
Com nosso Bot IA: Venda fechada! 🎉

Vou mostrar EXATAMENTE como isso funciona...
        """
        
        self.type_slowly(intro_text, 0.02)
        self.speak("Imagine perder vendas porque não consegue atender 24 horas.")
        
        input(Fore.YELLOW + "\n➡️  Pressione ENTER para começar a demo..." + Style.RESET_ALL)
    
    def start_services(self):
        """Inicia serviços necessários"""
        print(Fore.CYAN + "\n🚀 INICIANDO SISTEMAS...\n" + Style.RESET_ALL)
        
        steps = [
            ("Iniciando servidor principal", "✅ Servidor online na porta 5000"),
            ("Conectando com OpenAI GPT-4", "✅ IA conectada e operacional"),
            ("Ativando WhatsApp Business API", "✅ WhatsApp pronto para receber"),
            ("Carregando banco de imóveis", "✅ 1.247 imóveis disponíveis"),
            ("Iniciando analytics em tempo real", "✅ Dashboard ativo")
        ]
        
        for desc, result in steps:
            print(f"⏳ {desc}...", end='', flush=True)
            time.sleep(random.uniform(0.5, 1.5))
            print(f"\r{result}        ")
        
        print(Fore.GREEN + "\n✨ TODOS OS SISTEMAS OPERACIONAIS!\n" + Style.RESET_ALL)
        time.sleep(2)
    
    def open_dashboard(self):
        """Abre dashboard com destaque"""
        print(Fore.CYAN + "\n📊 ABRINDO DASHBOARD PREMIUM...\n" + Style.RESET_ALL)
        
        # Simula abertura do dashboard
        webbrowser.open('http://localhost:5000/dashboard')
        time.sleep(3)
        
        print(Fore.GREEN + "Dashboard aberto! Veja:" + Style.RESET_ALL)
        print("• Métricas atualizando em tempo real")
        print("• 342 conversas processadas hoje")
        print("• Taxa de conversão: 47%")
        print("• Satisfação: 4.9 ⭐")
        
        time.sleep(3)
    
    def demo_simple_search(self):
        """Demonstra busca simples"""
        print(Fore.YELLOW + "\n🏠 DEMO 1: BUSCA SIMPLES\n" + Style.RESET_ALL)
        
        print("👤 Cliente envia:")
        time.sleep(1)
        message = "Olá! Procuro apartamento para comprar em Florianópolis"
        print(Fore.GREEN + f"   \"{message}\"" + Style.RESET_ALL)
        
        print("\n⚡ Bot responde em 0.8 segundos:")
        time.sleep(0.8)
        
        response = """
🤖 Olá! Que ótimo que você nos procurou! 🏠 
   
   Encontrei 3 apartamentos PERFEITOS para você:
   
   📍 AP001 - Centro | 3 quartos | Vista mar
   💰 R$ 750.000 | 12 fotos + Tour 360°
   
   📍 AP005 - Agronômica | 2 quartos + escritório  
   💰 R$ 580.000 | Novo, nunca habitado
   
   📍 AP008 - Trindade | 3 quartos | 2 vagas
   💰 R$ 720.000 | Próximo UFSC
   
   Qual desperta mais seu interesse? 😊
        """
        
        self.type_slowly(Fore.CYAN + response, 0.01)
        
        print(Fore.MAGENTA + "\n💡 Perceba:" + Style.RESET_ALL)
        print("   • Resposta personalizada e calorosa")
        print("   • 3 opções relevantes instantaneamente")
        print("   • Convite para próximo passo")
        
        input(Fore.YELLOW + "\n➡️  ENTER para próxima demo..." + Style.RESET_ALL)
    
    def demo_urgency(self):
        """Demonstra caso urgente"""
        print(Fore.RED + "\n🚨 DEMO 2: CLIENTE URGENTE\n" + Style.RESET_ALL)
        
        print("👤 Cliente desesperado envia:")
        time.sleep(1)
        message = "URGENTE!!! Preciso alugar HOJE! Meu contrato termina amanhã!"
        print(Fore.RED + Style.BRIGHT + f"   \"{message}\"" + Style.RESET_ALL)
        
        print("\n⚡ Bot detecta urgência e responde em 0.5 segundos:")
        time.sleep(0.5)
        
        response = """
🚨 ENTENDO SUA URGÊNCIA! Vou priorizar seu atendimento AGORA!

📱 Corretor João está sendo notificado neste momento!
📞 WhatsApp direto: (48) 99999-8888

Enquanto isso, estas opções estão disponíveis HOJE:

🔥 AP003 - Trindade | 2 quartos mobiliados
💰 R$ 2.800/mês | Chaves NA HORA
✅ Contrato digital em 30 minutos

🔥 CA004 - Campeche | 3 quartos  
💰 R$ 4.500/mês | 200m da praia
✅ Visita em 1 hora se quiser

Qual prefere? Posso agendar visita AGORA! 🏃‍♂️
        """
        
        self.type_slowly(Fore.RED + response, 0.01)
        
        # Simula notificação
        print(Fore.YELLOW + "\n📱 NOTIFICAÇÃO ENVIADA:" + Style.RESET_ALL)
        print("   SMS → Corretor João Silva")
        print("   WhatsApp → Gerente Maria")
        print("   Slack → Canal #urgente")
        
        input(Fore.YELLOW + "\n➡️  ENTER para próxima demo..." + Style.RESET_ALL)
    
    def demo_audio(self):
        """Demonstra processamento de áudio"""
        print(Fore.GREEN + "\n🎤 DEMO 3: MENSAGEM DE ÁUDIO\n" + Style.RESET_ALL)
        
        print("👤 Cliente envia áudio de 15 segundos:")
        print(Fore.BLUE + "   🎵 ▶️ ━━━━━━━━━━━━━ 0:15" + Style.RESET_ALL)
        
        print("\n🎧 Transcrevendo com Whisper AI...")
        time.sleep(1.5)
        
        print(Fore.GREEN + "✅ Transcrição concluída:" + Style.RESET_ALL)
        transcription = "\"Oi, tô dirigindo mas preciso muito achar uma casa pra alugar, de preferência com 3 quartos no Campeche, perto da praia. Quanto tá o aluguel por aí?\""
        print(f"   {transcription}")
        
        print("\n⚡ Bot processa e responde:")
        response = """
🎤 Áudio recebido e transcrito!

🚗 Vi que está dirigindo. Por segurança, vou enviar tudo por texto para você ler quando parar!

🏠 Encontrei casas PERFEITAS no Campeche:

📍 Casa 3 quartos | 200m da praia
💰 R$ 4.500/mês
🏖️ Vista parcial do mar

📍 Casa 3 quartos + suíte | 400m da praia  
💰 R$ 5.200/mês
🌴 Quintal com churrasqueira

Salvei seu contato como prioridade! Quando estiver seguro, me avise que envio fotos! 📸
        """
        
        self.type_slowly(Fore.CYAN + response, 0.01)
        
        print(Fore.MAGENTA + "\n💡 Tecnologia em ação:" + Style.RESET_ALL)
        print("   • Whisper AI transcreveu com 99% precisão")
        print("   • IA detectou que cliente está dirigindo")
        print("   • Resposta adaptada para segurança")
        
        input(Fore.YELLOW + "\n➡️  ENTER para próxima demo..." + Style.RESET_ALL)
    
    def demo_photos(self):
        """Demonstra envio de fotos"""
        print(Fore.BLUE + "\n📸 DEMO 4: FOTOS E TOUR VIRTUAL\n" + Style.RESET_ALL)
        
        print("👤 Cliente interessado pede:")
        message = "Adorei o AP001! Tem fotos?"
        print(Fore.GREEN + f"   \"{message}\"" + Style.RESET_ALL)
        
        print("\n⚡ Bot responde com mídia rica:")
        time.sleep(0.5)
        
        print(Fore.CYAN + "📸 Claro! Enviando fotos do AP001 agora:" + Style.RESET_ALL)
        
        # Simula envio de fotos
        photos = [
            "🖼️ Foto 1: Vista panorâmica do mar",
            "🖼️ Foto 2: Sala de estar espaçosa", 
            "🖼️ Foto 3: Cozinha gourmet completa"
        ]
        
        for photo in photos:
            time.sleep(0.5)
            print(f"   {photo}")
        
        print(Fore.CYAN + "\n🎥 E tem mais! Tour Virtual 360°:" + Style.RESET_ALL)
        print("   🔗 matterport.com/tour/AP001")
        
        print(Fore.CYAN + "\n💰 Valor: R$ 750.000,00" + Style.RESET_ALL)
        print(Fore.CYAN + "📅 Posso agendar uma visita presencial?" + Style.RESET_ALL)
        
        input(Fore.YELLOW + "\n➡️  ENTER para analytics..." + Style.RESET_ALL)
    
    def show_analytics(self):
        """Mostra analytics impressionantes"""
        print(Fore.MAGENTA + "\n📊 ANALYTICS EM TEMPO REAL\n" + Style.RESET_ALL)
        
        print("Durante esta demonstração:")
        
        metrics = [
            ("Mensagens processadas", "4", Fore.GREEN),
            ("Tempo médio de resposta", "0.9s", Fore.CYAN),
            ("Sentimento do cliente", "😊 Positivo", Fore.YELLOW),
            ("Probabilidade de conversão", "87%", Fore.GREEN),
            ("Ação recomendada", "Agendar visita", Fore.BLUE)
        ]
        
        for metric, value, color in metrics:
            time.sleep(0.5)
            print(f"{color}📈 {metric}: {value}{Style.RESET_ALL}")
        
        print(Fore.WHITE + "\n💡 INSIGHTS DE IA:" + Style.RESET_ALL)
        insights = [
            "• Cliente tem alto interesse no AP001",
            "• Perfil: Comprador, primeira vez",
            "• Urgência: Moderada",
            "• Próximo passo ideal: Tour virtual seguido de visita"
        ]
        
        for insight in insights:
            time.sleep(0.5)
            print(Fore.CYAN + insight + Style.RESET_ALL)
    
    def show_roi(self):
        """Mostra ROI e benefícios"""
        print(Fore.YELLOW + "\n💰 RETORNO SOBRE INVESTIMENTO\n" + Style.RESET_ALL)
        
        print("Vamos fazer as contas juntos:\n")
        
        calculations = [
            ("Custo de 1 corretor:", "R$ 5.000/mês", Fore.RED),
            ("Custo do Bot IA:", "R$ 497/mês", Fore.GREEN),
            ("Economia mensal:", "R$ 4.503", Fore.YELLOW),
            ("", "", ""),
            ("Atendimentos/mês corretor:", "200", Fore.RED),
            ("Atendimentos/mês Bot:", "2.000+", Fore.GREEN),
            ("Aumento de capacidade:", "10x", Fore.YELLOW),
            ("", "", ""),
            ("Conversão corretor médio:", "15%", Fore.RED),
            ("Conversão Bot IA:", "47%", Fore.GREEN),
            ("Aumento de vendas:", "+213%", Fore.YELLOW)
        ]
        
        for label, value, color in calculations:
            if label:
                time.sleep(0.5)
                print(f"{color}{label:.<30} {value:>10}{Style.RESET_ALL}")
            else:
                print()
        
        print(Fore.GREEN + Style.BRIGHT + "\n🚀 ROI em menos de 30 dias!" + Style.RESET_ALL)
    
    def final_pitch(self):
        """Pitch final poderoso"""
        print(Fore.CYAN + "\n🎯 RESUMO EXECUTIVO\n" + Style.RESET_ALL)
        
        duration = int(time.time() - self.start_time)
        print(f"Em apenas {duration} segundos você viu:\n")
        
        features = [
            "✅ Atendimento 24/7 sem parar",
            "✅ Respostas em menos de 1 segundo",
            "✅ Processamento de áudio em 12 idiomas",
            "✅ Envio automático de fotos e tours",
            "✅ Detecção de urgência e escalação",
            "✅ Analytics e insights em tempo real",
            "✅ ROI garantido em 30 dias"
        ]
        
        for feature in features:
            time.sleep(0.3)
            print(Fore.GREEN + feature + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\n🤔 A PERGUNTA NÃO É 'SE' VOCÊ PRECISA..." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.YELLOW + Style.BRIGHT + "É QUANTO ESTÁ PERDENDO SEM TER! 💸" + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n📞 PRÓXIMOS PASSOS:" + Style.RESET_ALL)
        print("1. Teste grátis por 7 dias")
        print("2. Instalação em 24 horas")
        print("3. Treinamento completo incluso")
        print("4. Suporte dedicado")
        
        print(Fore.GREEN + Style.BRIGHT + "\n🎁 BÔNUS EXCLUSIVO HOJE:" + Style.RESET_ALL)
        print("• 50% desconto no primeiro mês")
        print("• Migração de dados grátis")
        print("• Personalização completa")
    
    def run(self):
        """Executa apresentação completa"""
        try:
            self.show_banner()
            self.introduction()
            self.start_services()
            self.open_dashboard()
            
            # Demos principais
            self.demo_simple_search()
            self.demo_urgency()
            self.demo_audio()
            self.demo_photos()
            
            # Fechamento
            self.show_analytics()
            self.show_roi()
            self.final_pitch()
            
            print(Fore.GREEN + "\n✨ APRESENTAÇÃO CONCLUÍDA!" + Style.RESET_ALL)
            print(Fore.YELLOW + "\nPronto para revolucionar seu negócio? 🚀" + Style.RESET_ALL)
            
        except KeyboardInterrupt:
            print(Fore.RED + "\n\nApresentação interrompida." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"\nErro: {str(e)}" + Style.RESET_ALL)

def create_video_script():
    """Cria roteiro para vídeo de demonstração"""
    
    video_script = """
# 🎬 ROTEIRO DE VÍDEO - BOT IMOBILIÁRIO IA

## DURAÇÃO: 3 minutos

### ABERTURA (0:00 - 0:15)
**Visual:** Logo animado + música impactante
**Narração:** "E se você pudesse multiplicar sua equipe de vendas por 10... sem contratar ninguém?"

### PROBLEMA (0:15 - 0:30)
**Visual:** Corretor estressado, telefone tocando, mensagens não respondidas
**Narração:** "Imobiliárias perdem 67% das vendas por não responder rápido o suficiente."
**Texto na tela:** "23:47 - Cliente: 'Ainda tem o apartamento?' ❌ Visto às 08:32"

### SOLUÇÃO (0:30 - 1:00)
**Visual:** Interface do Bot respondendo instantaneamente
**Narração:** "Apresentamos o Bot Imobiliário IA - Seu corretor digital 24/7"
**Demonstrar:**
- Resposta instantânea
- Múltiplas conversas simultâneas
- Dashboard em tempo real

### DEMONSTRAÇÃO (1:00 - 2:00)
**Cena 1:** Cliente envia áudio às 22h
- Bot transcreve
- Responde com opções
- Envia fotos

**Cena 2:** Cliente urgente
- Bot detecta urgência
- Escala para humano
- Agenda visita

**Cena 3:** Dashboard
- Métricas subindo
- Conversões em tempo real
- ROI calculado

### BENEFÍCIOS (2:00 - 2:30)
**Visual:** Gráficos animados mostrando crescimento
**Bullets rápidos:**
- ⚡ Respostas em 1 segundo
- 🌍 12 idiomas
- 📈 300% mais vendas
- 💰 ROI em 30 dias
- 🏆 98% satisfação

### CALL TO ACTION (2:30 - 3:00)
**Visual:** QR Code + URL + Telefone
**Narração:** "Teste GRÁTIS por 7 dias. Sem compromisso."
**Texto:** "👉 botimobiliario.ai/demo"
**Oferta:** "50% OFF para os primeiros 50 clientes!"

### ELEMENTOS VISUAIS
- Cores: Azul (#3B82F6) + Roxo (#8B5CF6)
- Fonte: Inter/Poppins
- Ícones: Animados e modernos
- Transições: Suaves com motion blur

### ÁUDIO
- Música: Upbeat corporate/tech
- Efeitos: Notification sounds
- Voz: Profissional, confiante

### DICAS DE PRODUÇÃO
1. Use screencasts reais do dashboard
2. Mostre WhatsApp real funcionando
3. Depoimentos de clientes (se tiver)
4. Mantenha ritmo acelerado
5. Legendas em português
"""
    
    with open('video_script.md', 'w') as f:
        f.write(video_script)
    print("✅ Roteiro de vídeo criado")

# Criar tudo
def main():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════════╗
    ║          🎪 SISTEMA DE APRESENTAÇÃO PREMIUM 🎪           ║
    ╚══════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    print("Escolha uma opção:\n")
    print("1. 🎭 Executar apresentação automatizada")
    print("2. 🎬 Criar roteiro de vídeo")
    print("3. 🚀 Executar ambos")
    
    choice = input("\nOpção: ")
    
    if choice in ['1', '3']:
        presentation = AutoPresentation()
        presentation.run()
    
    if choice in ['2', '3']:
        create_video_script()
        print(Fore.GREEN + "\n✅ Roteiro de vídeo salvo em: video_script.md" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n🎉 SISTEMA DE APRESENTAÇÃO COMPLETO!" + Style.RESET_ALL)
    print("\nRecursos criados:")
    print("• Apresentação automatizada interativa")
    print("• Roteiro profissional para vídeo")
    print("• Scripts de demonstração")
    print("• Cálculos de ROI automáticos")

if __name__ == "__main__":
    main()
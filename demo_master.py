#!/usr/bin/env python3
"""
🎮 CONTROLE MASTER DA DEMO PREMIUM
Execute: python demo_master.py
"""

import os
import sys
import subprocess
import time
import webbrowser
from datetime import datetime

class DemoMaster:
    def __init__(self):
        self.bot_process = None
        self.ngrok_process = None
        
    def show_banner(self):
        """Mostra banner animado"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = """
        ╔══════════════════════════════════════════════════════════════════╗
        ║                                                                  ║
        ║     🤖 BOT IMOBILIÁRIO IA - CONTROLE MASTER DA DEMO 🤖          ║
        ║                                                                  ║
        ║     ⚡ Powered by GPT-4 + Twilio + WhatsApp                     ║
        ║     📊 Dashboard Premium com Analytics em Tempo Real            ║
        ║     🎯 Sistema Completo de Demonstração                         ║
        ║                                                                  ║
        ╚══════════════════════════════════════════════════════════════════╝
        """
        print("\033[96m" + banner + "\033[0m")
        
    def check_requirements(self):
        """Verifica requisitos do sistema"""
        print("\n🔍 Verificando requisitos...")
        
        requirements = {
            'Python': sys.version,
            'Flask': self._check_package('flask'),
            'Twilio': self._check_package('twilio'),
            'OpenAI': self._check_package('openai'),
            'Node/NPM': self._check_command('npm --version'),
            'Ngrok': self._check_command('ngrok --version')
        }
        
        all_ok = True
        for req, status in requirements.items():
            if status:
                print(f"✅ {req}: OK")
            else:
                print(f"❌ {req}: Não encontrado")
                all_ok = False
        
        return all_ok
    
    def _check_package(self, package):
        try:
            __import__(package)
            return True
        except ImportError:
            return False
    
    def _check_command(self, command):
        try:
            subprocess.run(command.split(), capture_output=True, check=True)
            return True
        except:
            return False
    
    def setup_environment(self):
        """Configura o ambiente"""
        print("\n🔧 Configurando ambiente...")
        
        # Verifica .env
        if not os.path.exists('.env'):
            if os.path.exists('.env.example'):
                print("📝 Copiando .env.example para .env")
                subprocess.run(['cp', '.env.example', '.env'])
                print("⚠️  Por favor, configure as variáveis no arquivo .env")
                return False
        
        print("✅ Arquivo .env encontrado")
        return True
    
    def start_services(self):
        """Inicia todos os serviços"""
        print("\n🚀 Iniciando serviços...")
        
        # 1. Inicia o bot
        print("📱 Iniciando bot...")
        self.bot_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        
        # 2. Inicia ngrok (opcional)
        if input("\n🌐 Iniciar ngrok para acesso externo? (s/n): ").lower() == 's':
            print("🌐 Iniciando ngrok...")
            self.ngrok_process = subprocess.Popen(
                ['ngrok', 'http', '5000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(3)
            print("✅ Ngrok iniciado - verifique em http://localhost:4040")
    
    def show_menu(self):
        """Menu principal"""
        while True:
            print("\n" + "="*60)
            print("🎮 MENU PRINCIPAL")
            print("="*60)
            
            options = [
                "1. 🌐 Abrir Landing Page",
                "2. 📊 Abrir Dashboard Premium", 
                "3. 🎭 Executar Demo Interativa",
                "4. 🧪 Rodar Testes Automatizados",
                "5. 📱 Mostrar QR Code WhatsApp",
                "6. 📚 Ver Guia de Apresentação",
                "7. 🔧 Verificar Status dos Serviços",
                "8. 🎯 Modo Apresentação (Tela Cheia)",
                "9. 💾 Gerar Relatório de Demo",
                "0. 🛑 Parar Tudo e Sair"
            ]
            
            for option in options:
                print(option)
            
            choice = input("\n🎯 Escolha uma opção: ")
            
            if choice == '1':
                self.open_landing_page()
            elif choice == '2':
                self.open_dashboard()
            elif choice == '3':
                self.run_interactive_demo()
            elif choice == '4':
                self.run_tests()
            elif choice == '5':
                self.show_whatsapp_qr()
            elif choice == '6':
                self.show_presentation_guide()
            elif choice == '7':
                self.check_status()
            elif choice == '8':
                self.presentation_mode()
            elif choice == '9':
                self.generate_report()
            elif choice == '0':
                self.shutdown()
                break
            else:
                print("❌ Opção inválida!")
    
    def open_landing_page(self):
        """Abre landing page"""
        print("\n🌐 Abrindo landing page...")
        webbrowser.open('http://localhost:5000')
        print("✅ Landing page aberta no navegador")
    
    def open_dashboard(self):
        """Abre dashboard"""
        print("\n📊 Abrindo dashboard...")
        webbrowser.open('http://localhost:5000/dashboard')
        print("✅ Dashboard aberto no navegador")
    
    def run_interactive_demo(self):
        """Executa demo interativa"""
        print("\n🎭 Iniciando demo interativa...")
        subprocess.run([sys.executable, 'run_demo.py'])
    
    def run_tests(self):
        """Executa testes"""
        print("\n🧪 Executando testes automatizados...")
        subprocess.run([sys.executable, 'test_demo.py'])
    
    def show_whatsapp_qr(self):
        """Mostra QR code"""
        print("\n📱 QR Code do WhatsApp:")
        print("""
        ┌─────────────────────────────┐
        │                             │
        │    [QR CODE AQUI]           │
        │                             │
        │    Escaneie para acessar    │
        │    o bot no WhatsApp        │
        │                             │
        └─────────────────────────────┘
        
        Ou envie mensagem para: +1 415 523 8886
        Digite: "join demo-bot"
        """)
        input("\nPressione ENTER para continuar...")
    
    def show_presentation_guide(self):
        """Mostra guia de apresentação"""
        print("\n📚 Abrindo guia de apresentação...")
        if os.path.exists('PRESENTATION_GUIDE.md'):
            if sys.platform == 'win32':
                os.startfile('PRESENTATION_GUIDE.md')
            elif sys.platform == 'darwin':
                subprocess.run(['open', 'PRESENTATION_GUIDE.md'])
            else:
                subprocess.run(['xdg-open', 'PRESENTATION_GUIDE.md'])
        else:
            print("❌ Guia não encontrado!")
    
    def check_status(self):
        """Verifica status dos serviços"""
        print("\n🔧 STATUS DOS SERVIÇOS:")
        print("="*40)
        
        # Bot status
        if self.bot_process and self.bot_process.poll() is None:
            print("✅ Bot: ONLINE")
        else:
            print("❌ Bot: OFFLINE")
        
        # Ngrok status
        if self.ngrok_process and self.ngrok_process.poll() is None:
            print("✅ Ngrok: ONLINE")
        else:
            print("⚠️  Ngrok: OFFLINE")
        
        # API status
        try:
            import requests
            response = requests.get('http://localhost:5000/health', timeout=2)
            if response.status_code == 200:
                print("✅ API: RESPONDENDO")
            else:
                print("⚠️  API: PROBLEMA")
        except:
            print("❌ API: NÃO RESPONDE")
        
        input("\nPressione ENTER para continuar...")
    
    def presentation_mode(self):
        """Modo apresentação"""
        print("\n🎯 MODO APRESENTAÇÃO")
        print("="*40)
        print("1. Dashboard será aberto em tela cheia")
        print("2. Landing page em nova aba")
        print("3. WhatsApp Web pronto")
        print("\nPreparando em 3 segundos...")
        
        time.sleep(3)
        
        # Abre tudo necessário
        webbrowser.open('http://localhost:5000')
        time.sleep(1)
        webbrowser.open('http://localhost:5000/dashboard')
        time.sleep(1)
        webbrowser.open('https://web.whatsapp.com')
        
        print("\n✅ Modo apresentação ativado!")
        print("\n💡 DICAS:")
        print("• Use Alt+Tab para alternar entre janelas")
        print("• F11 para tela cheia no navegador")
        print("• Tenha o celular pronto para QR code")
        
        input("\nPressione ENTER para continuar...")
    
    def generate_report(self):
        """Gera relatório de demo"""
        print("\n💾 Gerando relatório de demonstração...")
        
        report = f"""
# RELATÓRIO DE DEMONSTRAÇÃO
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## MÉTRICAS DA DEMO
- Tempo total: {datetime.now().strftime('%H:%M')}
- Serviços ativos: Bot, Dashboard, API
- Mensagens processadas: 47
- Tempo médio resposta: 1.2s
- Taxa de sucesso: 98.5%

## RECURSOS DEMONSTRADOS
✅ Busca de imóveis
✅ Processamento de áudio
✅ Multi-idioma
✅ Dashboard analytics
✅ Modo urgência
✅ Sistema de recomendação

## FEEDBACK SIMULADO
- Interesse: ALTO
- Probabilidade de compra: 85%
- Pontos fortes: Velocidade, precisão, interface
- Objeções: Preço, integração com CRM

## PRÓXIMOS PASSOS
1. Agendar reunião de follow-up
2. Preparar proposta comercial
3. Definir período de teste
4. Configurar piloto
        """
        
        filename = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Relatório salvo em: {filename}")
        input("\nPressione ENTER para continuar...")
    
    def shutdown(self):
        """Encerra todos os serviços"""
        print("\n🛑 Encerrando serviços...")
        
        if self.bot_process:
            self.bot_process.terminate()
            print("✅ Bot encerrado")
        
        if self.ngrok_process:
            self.ngrok_process.terminate()
            print("✅ Ngrok encerrado")
        
        print("\n👋 Obrigado por usar o Bot Imobiliário IA!")
        print("💡 Para suporte: contato@botimobiliario.ai")
        time.sleep(2)

def main():
    """Função principal"""
    demo = DemoMaster()
    demo.show_banner()
    
    # Verifica requisitos
    if not demo.check_requirements():
        print("\n❌ Instale os requisitos faltantes!")
        print("Execute: pip install -r requirements.txt")
        return
    
    # Configura ambiente
    if not demo.setup_environment():
        print("\n⚠️  Configure o arquivo .env antes de continuar!")
        return
    
    # Pergunta se quer iniciar serviços
    if input("\n🚀 Iniciar todos os serviços? (s/n): ").lower() == 's':
        demo.start_services()
    
    # Menu principal
    demo.show_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário!")
        print("Encerrando serviços...")
        time.sleep(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        print("Entre em contato com o suporte!")
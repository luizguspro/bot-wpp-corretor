#!/usr/bin/env python3
"""
Script para corrigir TODOS os dados do bot
"""

import json
import os

def fix_all_data():
    print("🔧 Corrigindo todos os dados do bot...")
    
    # 1. Criar pasta data se não existir
    os.makedirs('data', exist_ok=True)
    
    # 2. Dados completos dos imóveis
    properties = [
        {
            "codigo": "AP001",
            "tipo": "Apartamento",
            "operacao": "venda",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "quartos": 3,
            "suites": 1,
            "preco": "750.000,00",
            "descricao": "Apartamento com vista para o mar, 3 quartos sendo 1 suíte, 2 vagas de garagem.",
            "fotos": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"
            ],
            "tour_virtual": "https://my.matterport.com/show/?m=SxQL3iGyvQk"
        },
        {
            "codigo": "CA002",
            "tipo": "Casa",
            "operacao": "venda",
            "bairro": "Jurerê",
            "cidade": "Florianópolis",
            "quartos": 4,
            "suites": 3,
            "preco": "2.500.000,00",
            "descricao": "Casa em condomínio fechado, 4 suítes, piscina, churrasqueira, 4 vagas.",
            "fotos": [
                "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800",
                "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800"
            ]
        },
        {
            "codigo": "AP003",
            "tipo": "Apartamento",
            "operacao": "aluguel",
            "bairro": "Trindade",
            "cidade": "Florianópolis",
            "quartos": 2,
            "suites": 0,
            "preco": "2.800,00",
            "descricao": "Apartamento próximo à UFSC, 2 quartos, mobiliado, com vaga de garagem.",
            "fotos": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"
            ]
        },
        {
            "codigo": "CA004",
            "tipo": "Casa",
            "operacao": "aluguel",
            "bairro": "Campeche",
            "cidade": "Florianópolis",
            "quartos": 3,
            "suites": 1,
            "preco": "4.500,00",
            "descricao": "Casa a 200m da praia, 3 quartos sendo 1 suíte, quintal amplo.",
            "fotos": [
                "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=800"
            ]
        },
        {
            "codigo": "AP005",
            "tipo": "Apartamento",
            "operacao": "venda",
            "bairro": "Agronômica",
            "cidade": "Florianópolis",
            "quartos": 2,
            "suites": 1,
            "preco": "580.000,00",
            "descricao": "Apartamento novo, 2 quartos sendo 1 suíte, sacada com churrasqueira.",
            "fotos": [
                "https://images.unsplash.com/photo-1565182999561-18d7dc61c393?w=800"
            ]
        }
    ]
    
    # 3. Informações da empresa
    company_info = {
        "name": "Imobiliária Digital IA",
        "about": "Somos pioneiros em atendimento imobiliário com Inteligência Artificial. Nossa missão é revolucionar a forma como você encontra o imóvel dos seus sonhos, com tecnologia de ponta e atendimento personalizado 24/7.",
        "contact": {
            "phone": "(48) 3333-4444",
            "whatsapp": "(48) 99999-8888",
            "email": "contato@imobiliariadigital.com.br",
            "address": "Av. Tecnologia, 1000 - Centro, Florianópolis/SC",
            "hours": "Atendimento 24/7 via WhatsApp | Presencial: Seg-Sex 9h-18h"
        },
        "financing": "Oferecemos consultoria completa para financiamento imobiliário! Trabalhamos com os principais bancos: Caixa, BB, Santander, Bradesco e Itaú. Simulamos as melhores condições, com taxas a partir de 0,99% a.m. Acompanhamos todo o processo, desde a simulação até a chave na mão!",
        "services": [
            "Compra e venda de imóveis",
            "Locação residencial e comercial",
            "Avaliação imobiliária gratuita",
            "Tour virtual 360°",
            "Consultoria de investimentos",
            "Assessoria jurídica"
        ]
    }
    
    # 4. Salvar arquivos
    with open('data/properties.json', 'w', encoding='utf-8') as f:
        json.dump(properties, f, ensure_ascii=False, indent=2)
    print("✅ properties.json criado com 5 imóveis!")
    
    with open('data/company_info.json', 'w', encoding='utf-8') as f:
        json.dump(company_info, f, ensure_ascii=False, indent=2)
    print("✅ company_info.json criado!")
    
    # 5. Corrigir AI Service para responder corretamente
    ai_service_fix = '''import os
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def classify_intent(self, text: str) -> dict:
        """Classifica a intenção da mensagem"""
        try:
            # Detecção rápida de intenções comuns
            text_lower = text.lower()
            
            # Como vocês podem ajudar = info sobre a empresa
            if any(phrase in text_lower for phrase in ['como vocês', 'como vcs', 'o que fazem', 'quais serviços']):
                return {"intent": "company_info", "parameters": {"info_type": "about"}}
            
            # Busca de imóveis
            if any(word in text_lower for word in ['procuro', 'quero', 'preciso', 'busco']):
                params = {}
                if 'apartamento' in text_lower:
                    params['tipo'] = 'apartamento'
                elif 'casa' in text_lower:
                    params['tipo'] = 'casa'
                
                if 'comprar' in text_lower or 'venda' in text_lower:
                    params['operacao'] = 'venda'
                elif 'alugar' in text_lower or 'aluguel' in text_lower:
                    params['operacao'] = 'aluguel'
                
                # Extrai número de quartos
                import re
                quartos_match = re.search(r'(\d+)\s*quarto', text_lower)
                if quartos_match:
                    params['quartos'] = int(quartos_match.group(1))
                
                return {"intent": "property_search", "parameters": params}
            
            # Fotos
            if any(word in text_lower for word in ['foto', 'imagem', 'ver', 'mostra']):
                return {"intent": "show_photos", "parameters": {}}
            
            # Contato
            if any(word in text_lower for word in ['contato', 'telefone', 'endereço', 'horário']):
                return {"intent": "company_info", "parameters": {"info_type": "contato"}}
            
            # Financiamento
            if 'financiamento' in text_lower:
                return {"intent": "company_info", "parameters": {"info_type": "financiamento"}}
            
            # Script de vendas
            if 'script' in text_lower and any(word in text_lower for word in ['venda', 'corretor']):
                return {"intent": "sales_script", "parameters": {}}
            
            # Caso geral - usa GPT para classificar
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Classifique a intenção em:
                        - property_search: busca por imóveis
                        - company_info: informações sobre a empresa
                        - sales_script: ajuda com vendas
                        - general: outros assuntos
                        
                        Retorne JSON: {"intent": "categoria", "parameters": {}}"""
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Erro na classificação: {str(e)}")
            return {"intent": "general", "parameters": {}}
    
    def generate_response(self, text: str) -> str:
        """Gera resposta usando IA para casos gerais"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um assistente virtual de uma imobiliária.
                        Seja sempre educado, profissional e prestativo.
                        Responda de forma concisa e clara.
                        Sempre termine oferecendo ajuda para encontrar imóveis."""
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return "Como posso ajudar você a encontrar o imóvel ideal?"
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcreve áudio usando Whisper"""
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"
                )
            
            return transcript.text
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {str(e)}")
            return ""
'''
    
    # Salvar AI Service corrigido
    with open('services/ai_service.py', 'w', encoding='utf-8') as f:
        f.write(ai_service_fix)
    print("✅ ai_service.py corrigido!")
    
    print("\n🎉 TUDO CORRIGIDO!")
    print("\n🚀 Agora:")
    print("1. Reinicie o bot (Ctrl+C e python app.py)")
    print("2. Teste novamente as perguntas")
    print("\n✅ Deve funcionar:")
    print('- "Como vocês podem me ajudar?" → Info sobre a empresa')
    print('- "Procuro apartamento para comprar" → Lista apartamentos')
    print('- "Quero casa para alugar" → Lista casas')

if __name__ == "__main__":
    fix_all_data()
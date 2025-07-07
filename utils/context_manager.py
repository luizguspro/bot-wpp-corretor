import json
import os
from datetime import datetime, timedelta

class ContextManager:
    """Gerencia contexto das conversas para manter coerência"""
    
    def __init__(self):
        self.contexts = {}
        self.context_timeout = timedelta(hours=24)
    
    def get_context(self, user_id: str) -> dict:
        """Recupera contexto do usuário"""
        if user_id not in self.contexts:
            return {}
        
        context = self.contexts[user_id]
        
        # Verifica timeout
        if datetime.now() - context.get('last_update', datetime.now()) > self.context_timeout:
            self.clear_context(user_id)
            return {}
        
        return context.get('data', {})
    
    def set_context(self, user_id: str, data: dict):
        """Define novo contexto"""
        self.contexts[user_id] = {
            'data': data,
            'last_update': datetime.now()
        }
    
    def update_context(self, user_id: str, updates: dict):
        """Atualiza contexto existente"""
        current = self.get_context(user_id)
        current.update(updates)
        self.set_context(user_id, current)
    
    def clear_context(self, user_id: str):
        """Limpa contexto do usuário"""
        if user_id in self.contexts:
            del self.contexts[user_id]
    
    def save_to_file(self, filepath: str = 'contexts.json'):
        """Salva contextos em arquivo (opcional)"""
        data = {}
        for user_id, context in self.contexts.items():
            data[user_id] = {
                'data': context['data'],
                'last_update': context['last_update'].isoformat()
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load_from_file(self, filepath: str = 'contexts.json'):
        """Carrega contextos de arquivo (opcional)"""
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for user_id, context in data.items():
            self.contexts[user_id] = {
                'data': context['data'],
                'last_update': datetime.fromisoformat(context['last_update'])
            }

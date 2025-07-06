import datetime
from typing import Dict, List

class CalendarSystem:
    def __init__(self):
        self.appointments = {}
        self.available_slots = self.generate_slots()
    
    def generate_slots(self) -> List[Dict]:
        """Gera horários disponíveis para os próximos 7 dias"""
        slots = []
        for days in range(1, 8):
            date = datetime.date.today() + datetime.timedelta(days=days)
            if date.weekday() < 6:  # Segunda a Sábado
                for hour in [9, 10, 11, 14, 15, 16, 17]:
                    slots.append({
                        "date": date.strftime("%d/%m/%Y"),
                        "time": f"{hour}:00",
                        "available": True
                    })
        return slots
    
    def book_appointment(self, property_code: str, date: str, time: str, client_phone: str) -> Dict:
        """Agenda uma visita"""
        slot_key = f"{date}_{time}"
        
        if slot_key in self.appointments:
            return {"success": False, "message": "Horário já ocupado"}
        
        self.appointments[slot_key] = {
            "property": property_code,
            "client": client_phone,
            "confirmed": False
        }
        
        return {
            "success": True,
            "message": f"Visita agendada para {date} às {time}!\n\nVocê receberá uma confirmação em breve.",
            "confirmation_code": f"VIS{len(self.appointments):04d}"
        }
    
    def get_available_slots(self, date: str = None) -> str:
        """Retorna horários disponíveis formatados"""
        available = []
        for slot in self.available_slots[:10]:  # Mostra até 10 opções
            slot_key = f"{slot['date']}_{slot['time']}"
            if slot_key not in self.appointments:
                available.append(f"📅 {slot['date']} às {slot['time']}")
        
        if not available:
            return "Desculpe, não há horários disponíveis nos próximos dias."
        
        return "🗓️ *Horários disponíveis para visita:*\n\n" + "\n".join(available)

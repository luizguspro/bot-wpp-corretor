# Emojis como strings Unicode que funcionam no Windows
EMOJIS = {
    'casa': '\U0001F3E0',
    'smile': '\U0001F60A',
    'star': '\U00002728',
    'fire': '\U0001F525',
    'target': '\U0001F3AF',
    'trophy': '\U0001F3C6',
    'medal2': '\U0001F948',
    'medal3': '\U0001F949',
    'camera': '\U0001F4F8',
    'calendar': '\U0001F4C5',
    'phone': '\U0001F4F1',
    'money': '\U0001F4B0',
    'sparkles': '\U00002728',
    'rocket': '\U0001F680',
    'heart': '\U00002764',
    'check': '\U00002705',
    'location': '\U0001F4CD',
    'key': '\U0001F511',
    'sunrise': '\U0001F305',
    'beach': '\U0001F3D6',
    'city': '\U0001F3D9',
    'family': '\U0001F468\U0000200D\U0001F469\U0000200D\U0001F467\U0000200D\U0001F466',
    'muscle': '\U0001F4AA',
    'party': '\U0001F389',
    'wave': '\U0001F44B',
    'thinking': '\U0001F914',
    'wink': '\U0001F609',
    'cool': '\U0001F60E',
    'crown': '\U0001F451',
    'diamond': '\U0001F48E',
    'alarm': '\U0001F6A8',
    'bulb': '\U0001F4A1',
    'sweat': '\U0001F605'
}

def e(name):
    """Helper para pegar emoji facilmente"""
    return EMOJIS.get(name, '')

from deep_translator import GoogleTranslator

def translate_text(text):
    return GoogleTranslator(source='auto', target='ru').translate(text)

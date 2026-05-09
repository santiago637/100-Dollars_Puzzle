import time
import requests
from datetime import datetime, timedelta

ULTIMO_PING = datetime.now()

def registrar_ping():
    global ULTIMO_PING
    ULTIMO_PING = datetime.now()

def enviar_mensaje_whatsapp():
    url = "https://graph.facebook.com/v17.0/TU_NUMERO_DE_WSP/messages"
    headers = {
        "Authorization": "Bearer TU_TOKEN",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "NUMERO_DE_TU_MAMA",
        "type": "text",
        "text": {"body": "Santiago no tiene internet 😅"}
    }
    requests.post(url, headers=headers, json=data)

def monitor():
    while True:
        ahora = datetime.now()
        if ahora - ULTIMO_PING > timedelta(minutes=15):
            enviar_mensaje_whatsapp()
        time.sleep(600)  # 10 minutos

monitor()

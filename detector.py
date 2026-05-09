from flask import Flask
import threading
import time
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

ULTIMO_PING = datetime.now()

# -----------------------------
# 1. Endpoint para recibir ping
# -----------------------------
@app.route("/ping")
def ping():
    global ULTIMO_PING
    ULTIMO_PING = datetime.now()
    return "OK", 200

# -----------------------------
# 2. Enviar WhatsApp
# -----------------------------
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

# -----------------------------
# 3. Monitor cada 10 minutos
# -----------------------------
def monitor():
    global ULTIMO_PING
    while True:
        ahora = datetime.now()
        hora = ahora.hour

        # Solo entre 2 pm y 10 pm
        if 14 <= hora < 22:
            if ahora - ULTIMO_PING > timedelta(minutes=15):
                enviar_mensaje_whatsapp()

        time.sleep(600)  # 10 minutos

# Hilo del monitor
threading.Thread(target=monitor, daemon=True).start()

# -----------------------------
# 4. Iniciar servidor Flask
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask
import threading
import time
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Última vez que la PC reportó estar viva
ULTIMO_PING = datetime.now()
# Flag para saber si se debe ignorar alerta por apagado normal
IGNORAR_ALERTA = False

# -----------------------------
# 1. Endpoint: ping normal
# -----------------------------
@app.route("/ping")
def ping():
    global ULTIMO_PING, IGNORAR_ALERTA
    ULTIMO_PING = datetime.now()
    IGNORAR_ALERTA = False
    print(f"[{ULTIMO_PING}] Ping recibido")
    return "OK", 200

# -----------------------------
# 2. Endpoint: apagando PC
# -----------------------------
@app.route("/shutdown")
def shutdown():
    global ULTIMO_PING, IGNORAR_ALERTA
    ULTIMO_PING = datetime.now()
    IGNORAR_ALERTA = True
    print(f"[{ULTIMO_PING}] PC apagándose, ignorar alerta")
    return "OK", 200

# -----------------------------
# 3. Enviar WhatsApp
# -----------------------------
def enviar_mensaje_whatsapp():
    url = "https://graph.facebook.com/v25.0/1093054933893080/messages"
    headers = {
        "Authorization": "Bearer EAAQocp84KbUBRaL032tpnV4FSRygbleMiAf1iXtGAZBXgguuZCDQ620uR0wLHndAUlsfhGlEVXotRBreVLgOmItTzNA8PGYZBImmEtbVJ8ZBGxDZAMuudZAZCqe9uR7noB8eafTZCffc4ZAgRsDQWQZAJLG6KEZBohkyYA6t9uAInXc2ZCZCO816ceiik2dLFtZBT86POuCvjmASMfcYfOAXiqAJclZAdiHqSTgoqBp92v10MlH1mMNMLJL7cKvvWqT41lIvE8rvyLUWiB3RsKoeLPQMrwANmFL1QZDZD",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "584247431917",
        "type": "text",
        "text": {"body": "Santiago parece estar sin internet o su PC se cayó."}
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        print("WhatsApp enviado, status:", r.status_code, r.text)
    except Exception as e:
        print("Error enviando WhatsApp:", e)

# -----------------------------
# 4. Monitor en segundo plano
# -----------------------------
def monitor():
    global ULTIMO_PING, IGNORAR_ALERTA
    while True:
        ahora = datetime.now()
        hora = ahora.hour

        # Solo monitorear entre 2 pm y 10 pm
        if 14 <= hora < 22:
            diferencia = ahora - ULTIMO_PING

            # Si han pasado más de 15 minutos sin ping
            if diferencia > timedelta(minutes=15):
                if not IGNORAR_ALERTA:
                    print(f"[{ahora}] Sin ping por {diferencia}, enviando WhatsApp...")
                    enviar_mensaje_whatsapp()
                    # Para no spamear, esperar 20 minutos antes de volver a alertar
                    time.sleep(1200)
                else:
                    print(f"[{ahora}] Sin ping pero IGNORAR_ALERTA=True, no se envía WhatsApp")
        time.sleep(600)  # Revisar cada 10 minutos

# Lanzar monitor en hilo aparte
threading.Thread(target=monitor, daemon=True).start()

# -----------------------------
# 5. Iniciar servidor Flask
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

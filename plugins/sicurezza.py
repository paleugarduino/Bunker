# plugins/sicurezza.py
import socket
from bunker_base import ComponenteBase

class PluginSicurezza(ComponenteBase):
    def __init__(self, nome, servizi):
        # 🔌 Connessione vitale ai servizi del Kernel
        self.nome = nome
        self.servizi = servizi

    def esegui(self, parametro):
        vademecum = "🛡️ **PROTOCOLLO OMBRA**: Verifica varco 9150 e IP Ghost."
        self.servizi.elsa.put(("sistema", vademecum))

        # 1. Verifica fisica della porta (Socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", 9150)) != 0:
                self.servizi.elsa.put(("sistema", "🚨 **ALLERTA**: Varco 9150 chiuso."))
                return {"stato": "KO", "dati": "TOR non rilevato."}

        # 2. Verifica logica del traffico (Requests)
        try:
            # Controllo se tor_api esiste prima di sparare
            if not self.servizi.tor_api:
                return {"stato": "KO", "dati": "Errore: tor_api non inizializzato nel Kernel."}
                
            res = self.servizi.tor_api.get("https://api.ipify.org?format=json", timeout=10)
            ip = res.json().get("ip")
            self.servizi.elsa.put(("sistema", f"✅ **DIFESA**: Tunnel attivo. IP: {ip}"))
            return {"stato": "OK", "dati": f"Invisibile. IP: {ip}"}
        except Exception as e:
            return {"stato": "KO", "dati": f"Varco aperto ma bloccato: {e}"}

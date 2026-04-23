import time
import os
import requests
from bunker_base import ComponenteBase

class PluginTatto(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        # Il Tatto opera sullo stesso browser usato dall'Esploratore
        print(f"🖐️ [SISTEMA-TATTILE] Calibrato. Modalità: Interazione Testuale Attiva.")

    def _ottieni_browser(self):
        """Recupera l'istanza attiva del browser dal motore."""
        return self.servizi.motore.esplora

    def clicca(self, selettore):
        """Esegue un clic fisico su un elemento specifico via CSS."""
        browser = self._ottieni_browser()
        elemento = browser.ele(selettore)
        if elemento:
            elemento.click()
            return f"✅ Clic eseguito su: {selettore}"
        return f"❌ Elemento {selettore} non trovato."

    def clicca_testo(self, testo_target):
        """
        MODIFICA STRATEGICA: Clicca su un link o bottone basandosi sul TESTO.
        Permette ad Elsa di muoversi seguendo le etichette testuali.
        """
        browser = self._ottieni_browser()
        # Cerca l'elemento che contiene esattamente o parzialmente il testo
        elemento = browser.ele(f"text={testo_target}")
        if elemento:
            elemento.click()
            return f"✅ Clic eseguito sul testo: '{testo_target}'"
        return f"❌ Nessun elemento con testo '{testo_target}' rilevato."

    def scrivi(self, selettore, testo):
        """Inserisce testo in un campo (es. login o form)."""
        browser = self._ottieni_browser()
        campo = browser.ele(selettore)
        if campo:
            campo.input(testo)
            return f"✅ Inserito testo in: {selettore}"
        return f"❌ Campo {selettore} non trovato."

    def muovi_navigazione(self, direzione):
        """Gestisce i tasti Avanti, Indietro (Prev) e Refresh."""
        browser = self._ottieni_browser()
        # Unificazione dei segnali di navigazione
        if direzione in ["back", "prev"]:
            browser.back()
        elif direzione in ["forward", "next"]:
            browser.forward()
        elif direzione == "refresh":
            browser.refresh()
        return f"✅ Navigazione eseguita: {direzione}"

    def scarica_risorsa(self, url, nome_file):
        """Scarica fisicamente un media nel Bunker tramite tunnel Tor."""
        path = f"Memoria/Amante_inamorata/Media/{nome_file}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            session = requests.Session()
            session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            r = session.get(url, stream=True, timeout=30)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024): f.write(chunk)
                return f"✅ Risorsa acquisita: {path}"
            return f"❌ Errore download: HTTP {r.status_code}"
        except Exception as e:
            return f"🚨 Avaria acquisizione: {str(e)}"
            
    def esegui(self, pacchetto_elsa):
        """
        Dispatcher Tattile: cmd[tatto|azione|parametro]
        """
        try:
            parti = pacchetto_elsa.replace('cmd[tatto|', '').replace(']', '').split('|')
            azione = parti[0].lower()
            param = parti[1] if len(parti) > 1 else ""

            # Mapping delle azioni unificate
            if azione == "clicca": return {"stato": "OK", "dati": self.clicca(param)}
            
            # Nuova rotta per il movimento testuale
            if azione == "clicca_testo": return {"stato": "OK", "dati": self.clicca_testo(param)}
            
            if azione == "scrivi": 
                testo = parti[2] if len(parti) > 2 else ""
                return {"stato": "OK", "dati": self.scrivi(param, testo)}
            
            if azione == "scarica":
                nome = parti[2] if len(parti) > 2 else "file_acquisito"
                return {"stato": "OK", "dati": self.scarica_risorsa(param, nome)}
            
            if azione in ["back", "prev", "forward", "next", "refresh"]: 
                return {"stato": "OK", "dati": self.muovi_navigazione(azione)}
            
            return {"stato": "KO", "dati": "Azione tattile non riconosciuta."}
        except Exception as e:
            return {"stato": "KO", "dati": f"Avaria Tattile: {str(e)}"}

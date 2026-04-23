import re
from bunker_base import Services

import re
from bunker_base import Services

class BunkerEngine:
    def __init__(self, elsa, db, tor_api, esplora, app, browser=None):
        # 🧠 Compatibilità legacy (opzionale)
        self.browser_session = browser
 
        self.output_queue = elsa
        self.memory_manager = db
        self.esplora = esplora
        
        self.servizi = Services(self, app=app)
        self.plugins = {}
        self.permessi_plugin = {}  # Verrà iniettato dall'Orchestratore
         
    def aggiungi_plugin(self, nome, classe_plugin):
        print(f"DEBUG: Caricamento plugin {nome}...")
        self.plugins[nome] = classe_plugin(nome, self.servizi)

    def esegui_plugin(self, nome_modulo, argomento):
        """Metodo vitale per permettere alla Percezione di innescare gli altri moduli."""
        if nome_modulo in self.plugins:
            return self.plugins[nome_modulo].esegui(argomento)
        return {"stato": "KO", "dati": f"Modulo '{nome_modulo}' inesistente."}

    def elabora(self, testo_da_regina):
        """Filtra il testo tramite la percezione e lo restituisce pulito."""
        testo_protetto = re.sub(r'cmd\[.*?\]', '', testo_da_regina).strip()
        
        if not testo_protetto:
            return ""
        
        if "percezione" not in self.plugins:
            return testo_da_regina
            
        testo_pulito = self.plugins["percezione"].esegui(testo_da_regina)
        return testo_pulito

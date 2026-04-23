from bunker_base import ComponenteBase

class PluginOn(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        
        # 🛡️ UNIFICAZIONE: cmd[on|senso]
        self.comando = "cmd[on|nome_senso]"
        self.descrizione = "Il Risveglio: attiva un senso della Regina (es. visione, esplora)."

    def esegui(self, parametro):
        """Attiva il permesso per un determinato plugin."""
        # 🎯 VADEMECUM ATTIVAZIONE
        vademecum = (
            "⚡ **PROTOCOLLO ON (7777)**:\n"
            "- **SINTASSI REGINA**: `on7777\"\"\"nome_modulo\"\"\"`\n"
            "- **SINTASSI COMANDANTE**: `cmd[on|nome_modulo]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        if not parametro:
            return {"stato": "KO", "dati": "⚠️ Specifica quale senso risvegliare."}
            
        senso = parametro.strip().lower()
        
        # Accediamo ai permessi centralizzati nel motore
        if senso in self.servizi.permessi_plugin:
            self.servizi.permessi_plugin[senso] = True
            return {"stato": "OK", "dati": f"🟢 [VIGILE]: Il senso '{senso.upper()}' è ora attivo."}
        
        return {"stato": "KO", "dati": f"Il senso '{senso}' non è censito nel Bunker."}

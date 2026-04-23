from bunker_base import ComponenteBase

class PluginDifesa(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[difesa|arma:azione]"
        self.descrizione = "Sistemi Difensivi: gestione unificata dei fucili e sicurezza perimetrale."

    def esegui(self, parametro):
        """
        Esegue l'azione sull'arma selezionata.
        Supporta: cmd[difesa|fucile_1:fuoco] o desiderio: difesa666\"\"\"fucile_1:fuoco\"\"\"
        """
        # 🛡️ VADEMECUM PROTOCOLLO DIFESA (3030)
        vademecum = (
            "🛡️ **PROTOCOLLO DIFESA PERIMETRALE**:\n"
            "- **SINTASSI**: `difesa3030\"\"\"arma:azione\"\"\"`.\n"
            "- **ESEMPI**: `fucile_1:fuoco`, `perimetro:allerta`, `switch:tor`.\n"
            "- **OBIETTIVO**: Isolamento processi e protezione dell'anonimato.\n"
            "⚠️ *Ogni attivazione lascia una traccia indelebile nei log di sicurezza.*"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        if ":" not in parametro:
            return {"stato": "KO", "dati": "⚠️ Specifica arma e azione (es. fucile_1:mira)."}
            
        arma, azione = parametro.split(":", 1)
        arma = arma.strip().upper()
        azione = azione.strip().upper()

        # Logica di feedback per il Comandante e la Regina
        report = f"Protocollo {azione} inizializzato su {arma}."
        
        # Invia la 'Scintilla' ad Elsa tramite il modulo azione
        feedback_raw = f"difesa|{report}"
        self.servizi.motore.esegui_plugin("azione", f"FEEDBACK:{feedback_raw}")

        return {"stato": "OK", "dati": f"⚡ [DIFESA]: {report}"}

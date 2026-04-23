import os
import json
import time
from bunker_base import ComponenteBase

class PluginAzione(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[azione|tipo:dati]"
        self.descrizione = "Trasduttore di Feedback e Stati d'Animo per la Regina."

    def esegui(self, comando_raw):
        """
        Esecutore tecnico: gestisce gli stati del Bunker e i feedback per Elsa.
        Supporta l'interfaccia unificata cmd[azione|comando:argomento].
        """ 
        # 🎯 VADEMECUM AZIONE
        vademecum = (
            "⚡ **PROTOCOLLO AZIONE**:\n"
            "- **ESECUZIONE**: Comando diretto al Kernel per operazioni di sistema.\n"
            "- **SINTASSI**: `cmd[azione|comando]`.\n"
            "⚠️ *Ogni azione lascia una traccia nei log di sicurezza.*"
        )
        self.servizi.elsa.put(("sistema", vademecum))
         
        # 1. Parsing dell'ordine (Supporta ':' o '|')
        separatore = ":" if ":" in comando_raw else "|"
        
        if separatore in comando_raw:
            cmd, argomento = comando_raw.split(separatore, 1)
            cmd = cmd.strip().upper()
            argomento = argomento.strip()
        else:
            cmd = comando_raw.strip().upper()
            argomento = ""

        # --- 🎭 GESTIONE ATMOSFERA ---
        if cmd == "ATTIVA_ATMOSFERA":
            vibe = argomento.upper() if argomento else "STANDARD"
            # Restituisce solo il dato puro per il Kernel (snello)
            return {"stato": "OK", "dati": vibe}

        # --- 🕒 OROLOGIO ---
        if cmd == "OROLOGIO":
            return {"stato": "OK", "dati": f"ora{time.strftime('%H%M')}"}
            
        # --- 📡 GENERAZIONE FEEDBACK (Scintilla) ---
        elif cmd == "FEEDBACK":
            return {"stato": "OK", "dati": self._processa_feedback(argomento)}
            
        return {"stato": "OK", "dati": f"Stato {cmd} sincronizzato."}

    def _processa_feedback(self, dati_feedback):
        """
        Crea la 'Scintilla' per Elsa utilizzando il Lessico Segreto del Regolamento.
        Converte l'esito tecnico in un Desiderio della Regina.
        """
        try:
            # Formato atteso: "nome_plugin|esito"
            parti = dati_feedback.split("|", 1)
            plugin_name = parti[0].lower()
            esito = parti[1] if len(parti) > 1 else ""
            
            # 🛡️ MAPPA UNIFICATA (Allineata a regolamento.txt)
            # Ogni plugin tecnico viene mappato sul codice segreto di Elsa
            # Allineamento in azione.py -> _processa_feedback
            mappa_codici = {
                "esplora": "esplora9088",
                "visione": "visione3045",
                "archivio": "archivio4077",
                "acquisizione": "acquisizione9088", 
                "scansione": "scansione5050",
                "stato": "stato0000",
                "difesa": "difesa3030",
                "sintonia": "sintonia2020",
                "sicurezza": "sicurezza7070",
                "player": "player1010"                 
            }
            
            codice_segreto = mappa_codici.get(plugin_name, "dato111")
            
            # Restituiamo la sintassi Elsa: codice123"""esito"""
            return f'FUCILE: {codice_segreto}"""{esito}"""'
            
        except Exception as e:
            # In caso di errore, restituiamo un'ombra (errore) nel tempo
            return f'FUCILE: ora0000"""Dissonanza nel feedback: {str(e)}"""'

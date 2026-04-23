import os
import json

# ⚙️ Calibrazione della Testina di Lettura
BASE_PATH = os.path.join("Memoria", "Amante_inamorata", "Sessione", "Scrivania")
INDICE_PATH = os.path.join(BASE_PATH, "registro_canali.json")
DIMENSIONE_SEGMENTO = 1500

class PluginPlayer:
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi

    def esegui(self, argomento):
        if not argomento:
            return {"stato": "ERRORE", "dati": "Il Player è acceso, ma manca la cassetta. Usa 'indice' o 'leggi|canale|x|y'."}

        parti = argomento.strip().split('|')
        
        # 🛡️ SCUDO ANTI-BALBUZIE (Nuovo Innesto)
        # Se il Kernel per errore ha incollato "player|" all'inizio, lo rimuoviamo all'istante
        if parti[0].lower() == "player":
            parti.pop(0)
            
        # Ora estraiamo l'azione reale in totale purezza
        azione = parti[0].lower()

        if azione == "indice":
            return self._mostra_indice()
        elif azione == "leggi":
            if len(parti) < 4:
                return {"stato": "ERRORE", "dati": "Formato testina errato. Usa: leggi|canale|x|y (es. leggi|web|1|0)"}
            return self._leggi_segmento(canale=parti[1].lower(), x=parti[2], y=parti[3])
        else:
            return {"stato": "ERRORE", "dati": f"Azione '{azione}' non riconosciuta. Usa 'indice' o 'leggi'."}

    def _mostra_indice(self):
        """Mostra i nastri disponibili consultando il registro centrale."""
        path_reale = self.servizi.app.scrivania.path_indice
        
        if not os.path.exists(path_reale):
            return {"stato": "OK", "dati": "📭 La Scrivania è completamente vuota."}
            
        try:
            # 🛡️ ARMATURA: errors="replace" per evitare crash su caratteri ignoti
            with open(path_reale, "r", encoding="utf-8", errors="replace") as f:
                registro = json.load(f)
                
            riassunto = "🗂️ **INDICE DELLA SCRIVANIA (NASTRI PRONTI)**\n\n"
            elementi_trovati = 0
            
            for canale, nastri in registro.items():
                if nastri:
                    riassunto += f"📻 **CANALE {canale.upper()}**:\n"
                    for x, dati in nastri.items():
                        riassunto += f"  • [x={x}] ➔ Sorgente: *{dati['sorgente']}* (Segmenti totali: `y={dati['totale_segmenti_y']}`)\n"
                        elementi_trovati += 1
                    riassunto += "\n"
                    
            if elementi_trovati == 0:
                return {"stato": "OK", "dati": "📭 I 6 Canali sono aperti, ma i nastri sono ancora vuoti."}
                
            riassunto += "💡 **Istruzioni**: Per leggere il primo segmento, usa: `player1010\"\"\"leggi|canale|x|0\"\"\"`"
            return {"stato": "OK", "dati": f"[PLY]\n{riassunto}"}

        except Exception as e:
            return {"stato": "ERRORE", "dati": f"Nastro indice inceppato: {e}"}

    def _leggi_segmento(self, canale, x, y):
        """Innesca la testina di lettura centralizzata della Scrivania."""
        try:
            # Richiamiamo la logica sicura e allineata presente nel modulo BunkerScrivania
            risultato = self.servizi.app.scrivania.leggi_segmento(canale, x, y)
            
            # Verifichiamo se la Scrivania ha restituito un messaggio di errore
            if "⚠️ ERRORE" in risultato:
                return {"stato": "ERRORE", "dati": f"[PLY]\n{risultato}"}
            
            # Nel metodo _leggi_segmento, la restituzione dei dati ora è:
            return {"stato": "OK", "dati": f"[PLY] {risultato}"}
            
        except Exception as e:
             return {"stato": "ERRORE", "dati": f"Incisione illeggibile o errore di sistema: {e}"}

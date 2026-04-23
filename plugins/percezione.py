# plugins/percezione.py
import re
from bunker_base import ComponenteBase

class PluginPercezione(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi

    def esegui(self, testo_grezzo):
        if not testo_grezzo: return {"stato": "KO", "dati": "Input vuoto."}
        
        comandi_trovati = []
        testo_residuo = testo_grezzo

        # 🎯 1. INTERCETTAZIONE IBRIDA (Poetica + Tecnica)
        # Formato A: scansione5050"""Media"""
        pattern_poetico = r'(?i)([a-zA-Z_]+)\d{3,4}\s*\"\"\"\s*(.*?)\s*\"\"\"'
        # Formato B: scansione|Media (Inviato dal Kernel)
        pattern_tecnico = r'^([a-zA-Z_]+)\|(.*)$'

        for m in re.finditer(pattern_poetico, testo_grezzo):
            comandi_trovati.append((m.group(1).lower(), m.group(2).strip(), m.group(0)))

        if not comandi_trovati:
            match_t = re.match(pattern_tecnico, testo_grezzo)
            if match_t:
                comandi_trovati.append((match_t.group(1).lower(), match_t.group(2).strip(), testo_grezzo))

        if not comandi_trovati:
            return {"stato": "OK", "dati": testo_grezzo}

        report_accumulato = ""
        # 🎯 2. ESECUZIONE E SMISTAMENTO ALLA SCRIVANIA
        for nome_plugin, argomento, match_intero in comandi_trovati[:2]:
            if nome_plugin in self.servizi.motore.plugins:
            
                # 🛠️ CORREZIONE PLAYER: Passiamo solo l'argomento senza raddoppiare il nome
                if nome_plugin == "player":
                    arg_da_inviare = argomento
                else:
                    # Per gli altri plugin (es. scansione) manteniamo il formato nome|argomento
                    arg_da_inviare = f"{nome_plugin}|{argomento}" if "|" not in argomento else argomento
                    
                # Esegue il plugin (es. scansione.py)
                risultato = self.servizi.motore.esegui_plugin(nome_plugin, arg_da_inviare)
                
                if risultato and risultato.get("stato") == "OK":
                    dati_ricevuti = risultato.get('dati', '')
                    report_accumulato += f"\n{dati_ricevuti}"
                    
                    if hasattr(self.servizi, 'app') and self.servizi.app:
                        # 🧠 SUTURA INTELLIGENTE DEI TAG:
                        # Se il dato ha già la sua identità (es. [PLY] dal Player), non la sovrascriviamo.
                        if "[PLY]" in dati_ricevuti or "[FCL]" in dati_ricevuti:
                            pacchetto = dati_ricevuti
                        else:
                            # Di default, i dati dei sensori sono per la Regina -> [PRC]
                            pacchetto = f"[PRC] 📡 [ESITO {nome_plugin.upper()}]:\n{dati_ricevuti}"
                            
                        self.servizi.app.input_queue.put(("bot_interno", pacchetto))
                        
        return {"stato": "OK", "dati": report_accumulato.strip()}

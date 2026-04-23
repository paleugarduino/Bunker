import re
import json
import os

class BunkerParser:
    def __init__(self, path_vocabolario=None):
        # 🛡️ 1. REGEX UNIFICATA (Comandante e Kernel)
        self.REGEX_CMD = r"\[CMD\s*:\s*(\w+)\s*(?::\s*([^\]]+))?\]|cmd\[(\w+)(?:\|([^\]]+))?\]"
        
        # 👁️ 2. REGEX DESIDERI (Elsa: plugin123"""arg""")
        self.REGEX_DESIDERI = r"(\w+)\d{3,4}\"\"\"(.*?)\"\"\""
        
        self.mappa_ombra = {}
        if path_vocabolario and os.path.exists(path_vocabolario):
            with open(path_vocabolario, 'r', encoding='utf-8') as f:
                self.mappa_ombra = json.load(f)

    def purifica_ombra(self, testo_raw):
        """Trasforma il testo RAW (sporco) in CLEAN (per l'iniziazione)."""
        if not testo_raw: return ""
        testo_pulito = testo_raw
        for proibita, poetica in self.mappa_ombra.items():
            pattern = re.compile(rf"\b{re.escape(proibita)}\b", re.IGNORECASE)
            testo_pulito = pattern.sub(poetica, testo_pulito)
        return testo_pulito

    def split_per_agente(self, testo_raw):
        """Scompone il testo e unifica i comandi tecnici e i desideri poetici."""
        if not testo_raw: return []
        
        # Stippa FUCILE: e invia la stringa alla regina, 
        if testo_raw.startswith("FUCILE:"):
            return [testo_raw[7:].strip()]
        
        risultato_finale = []
        ultima_pos = 0

        # Unione dei match: Elsa ed il Comandante usano lo STESSO MOTORE
        matches = list(re.finditer(self.REGEX_CMD, testo_raw)) + \
                  list(re.finditer(self.REGEX_DESIDERI, testo_raw))
        matches.sort(key=lambda x: x.start())

        for match in matches:
            prosa = testo_raw[ultima_pos:match.start()].strip()
            if prosa: risultato_finale.append(prosa)

            groups = match.groups()
            if match.re.pattern == self.REGEX_CMD:
                # Comandante: [CMD:...] o cmd[...]
                nome = (groups[0] or groups[2]).lower()
                arg = (groups[1] or groups[3]) or ""
            else:
                # Regina: plugin123"""..."""
                nome = groups[0].lower()
                arg = groups[1]
            
            risultato_finale.append((nome, arg))
            ultima_pos = match.end()

        prosa_residua = testo_raw[ultima_pos:].strip()
        if prosa_residua: risultato_finale.append(prosa_residua)
        return risultato_finale

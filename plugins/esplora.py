import json
import os
import time
from bunker_base import ComponenteBase

class PluginEsplora(ComponenteBase):
    def __init__(self, nome, servizi):        
        self.nome = nome
        self.servizi = servizi
        self.memory_path = "Memoria/Amante_inamorata"
        self.max_pagine = 3 

        # 🧠 RECUPERO SENSI DAL KERNEL (SINGLETON)
        # Recuperiamo le istanze già caricate per evitare conflitti di memoria e crash
        self.visore = self.servizi.motore.plugins.get("visione_tattica")
        self.mano = self.servizi.motore.plugins.get("tatto")
        self.orecchio = self.servizi.motore.plugins.get("udito")
        
        print(f"🌐 [SISTEMA-ESPLORA] Sincronizzato con i sensi del Kernel.")

    def navigazione_ricognitiva(self, query):
        """AZIONE DEL BRACCIO: Navigazione ipertestuale e catalogazione media."""
        if not hasattr(self.servizi.motore, 'esplora'):
            return "🚨 ERRORE: Motore di navigazione non inizializzato."
            
        ombra = self.servizi.motore.esplora
        url = f"https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/?q={query.replace(' ', '+')}"
        
        ombra.get(url)
        reperti = {"link": [], "media": []} 
        
        for p in range(1, self.max_pagine + 1):
            ombra.scroll.to_bottom()
            time.sleep(2)
            
            # 1. Estrazione Ipertesto (Link)
            nodi = ombra.eles('css:article, .web-result, [data-testid="result"]')
            for el in nodi:
                link_tag = el.ele('css:a[data-testid="result-title-a"], h2 a')
                if link_tag:
                    url_trovato = link_tag.attr('href') or "URL_NON_DISPONIBILE"
                    reperti["link"].append({"titolo": link_tag.text, "url": url_trovato, "pagina": p})
            
            # 2. Estrazione Media
            risorse = ombra.eles('css:img, video, audio, source')
            for r in risorse:
                src = r.attr('src') or r.attr('data-src')
                if src and src not in [m['url'] for m in reperti["media"]]:
                    reperti["media"].append({
                        "tipo": r.tag, 
                        "url": src, 
                        "pagina": p, 
                        "alt": r.attr('alt') or "nessuna_descrizione"
                    })
            
            btn_next = ombra.ele('css:a[rel="next"], .result--more__btn')
            if btn_next and p < self.max_pagine:
                btn_next.click()
                time.sleep(2)
            else: break
            
        # Cattura screenshot solo per log
        temp_snap = os.path.join(self.memory_path, "Logs/temp_recon.png")
        os.makedirs(os.path.dirname(temp_snap), exist_ok=True)
        ombra.get_screenshot(path=temp_snap)
        
        # Archiviazione integrale dei reperti
        perc_ia = os.path.join(self.memory_path, "Ricerca/per_ia.json")
        with open(perc_ia, "w", encoding="utf-8") as f:
            json.dump(reperti, f, indent=4, ensure_ascii=False)
            
        return (f"✅ Ricognizione completata. Acquisiti {len(reperti['link'])} link "
                f"e {len(reperti['media'])} media. Visione in stand-by.")

    def esegui(self, pacchetto_elsa):
        # 🌐 VADEMECUM UNIFICATO ESPLORA (9088)
        vademecum = (
            "🌐 **PROTOCOLLO ESPLORA SATELLITARE (9088)**:\n"
            "- **NAVIGAZIONE**: `esplora9088\"\"\"vai_a|URL\"\"\"` o `\"\"\"query\"\"\"`.\n"
            "- **INGEGNERIA**: `esplora9088\"\"\"analizza_codice|focus\"\"\"`.\n"
            "- **ACCERTA**: `esplora9088\"\"\"accerta|prompt\"\"\"`.\n"
            "- **TATTO**: `esplora9088\"\"\"clicca_testo|etichetta\"\"\"` o `\"\"\"scrivi\"\"\"`.\n"
            "- **ACQUISIZIONE**: `esplora9088\"\"\"scarica|URL|nome\"\"\"`.\n"
            "- **UDITO**: `esplora9088\"\"\"ascolta|percorso|sec|temp|p|k\"\"\"`.\n"
            "⚠️ *Usa 'prev/back' per ritirarti e 'refresh' per sincronizzare.*"
        )
        self.servizi.elsa.put(("sistema", vademecum))

        try:
            corpo = pacchetto_elsa.replace('cmd[esplora|', '').replace(']', '')
            parti = [p.strip() for p in corpo.split('|')]
            azione = parti[0].lower()

            # Dispatcher verso i sensi (Mani)
            if azione in ["clicca", "clicca_testo", "scrivi", "back", "prev", "forward", "next", "refresh", "scarica"]:
                return self.mano.esegui(pacchetto_elsa.replace('esplora', 'tatto'))

            # Infiltrazione diretta
            if azione == "vai_a":
                url_target = parti[1]
                self.servizi.motore.esplora.get(url_target)
                return {"stato": "OK", "dati": f"✅ Infiltrazione eseguita su: {url_target}"}

            # Analisi Strutturale (Codice)
            if azione == "analizza_codice":
                struttura = self.servizi.motore.esplora.html 
                query = parti[1] if len(parti) > 1 else "Analisi Ingegneristica"
                return {"stato": "OK", "dati": self.visore.analizza_logica(struttura, query)}
            
            # Smistamento Visivo (Reale)
            if azione in ["vedi", "analizza", "oculi", "accerta", "verifica"]:
                temp_snap = os.path.join(self.memory_path, "Logs/verification.png")
                os.makedirs(os.path.dirname(temp_snap), exist_ok=True)
                self.servizi.motore.esplora.get_screenshot(path=temp_snap)
                prompt = parti[1] if len(parti) > 1 else "Esegui analisi forense di sicurezza."
                return {"stato": "OK", "dati": self.visore.analizza_reale(temp_snap, prompt)}
            
            # Smistamento Acustico
            if azione in ["ascolta", "udito", "intercetta"]:
                params = "|".join(parti[1:]) 
                return self.orecchio.esegui(params)
            
            # Navigazione Ricognitiva (Default)
            return {"stato": "OK", "dati": self.navigazione_ricognitiva(azione)}

        except Exception as e:
            return {"stato": "KO", "dati": f"Avaria Sistema Sensoriale: {str(e)}"}

import os
import requests
from urllib.parse import urlparse
import time
from bunker_base import ComponenteBase

class PluginAcquisizione(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[acquisizione|URL]"
        self.descrizione = "Mietitrebbia: Scarica, smista in sottocartelle e cataloga nell'archivio."

    def esegui(self, parametro):
        # 🎯 VADEMECUM ACQUISIZIONE
        vademecum = (
            "📥 **PROTOCOLLO ACQUISIZIONE (9088)**:\n"
            "- **OBIETTIVO**: Download file da URL esterni nel settore Media.\n"
            "- **SINTASSI REGINA**: `acquisizione9088\"\"\"URL\"\"\"`.\n"
            "- **SINTASSI COMANDANTE**: `cmd[acquisizione|URL]`.\n"
            "⚠️ *I file vengono salvati automaticamente nella radice di Media.*"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        if not parametro: return {"stato": "KO", "dati": "⚠️ URL mancante."}
        url = parametro.strip()
        nome_file = os.path.basename(urlparse(url).path)
        if not nome_file: nome_file = f"download_{int(time.time())}.data"
        
        # 📂 LOGICA DI SMISTAMENTO
        ext = os.path.splitext(nome_file)[1].lower()
        cartella = "Documenti"
        if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']: cartella = "Immagini"
        elif ext in ['.mp4', '.mkv', '.avi', '.mov']: cartella = "Video"
        elif ext in ['.mp3', '.wav', '.flac']: cartella = "Musica"

        target_dir = os.path.join(self.servizi.path_media, cartella)
        os.makedirs(target_dir, exist_ok=True)
        percorso_finale = os.path.join(target_dir, nome_file).replace("\\", "/")

        try:
            r = self.servizi.tor_api.get(url, stream=True, timeout=30)
            r.raise_for_status()
            with open(percorso_finale, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
            
            # 📚 AUTO-CATALOGAZIONE: Informiamo la Biblioteca
            nota = f"aggiungi|{percorso_finale}|File acquisito dal web: {url}"
            self.servizi.motore.esegui_plugin("archivio", nota)
            
            return {"stato": "OK", "dati": percorso_finale}
        except Exception as e:
            return {"stato": "KO", "dati": f"❌ Fallimento acquisizione: {e}"}

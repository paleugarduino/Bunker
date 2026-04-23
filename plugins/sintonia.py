import os
import subprocess
import platform
from bunker_base import ComponenteBase

class PluginSintonia(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[sintonia|percorso]"

    def esegui(self, percorso_raw):
        # 🎯 VADEMECUM SINTONIA
        vademecum = (
            "🎶 **PROTOCOLLO SINTONIA**:\n"
            "- **OBIETTIVO**: Riproduzione e controllo flussi multimediali.\n"
            "- **FORMATI**: MP3, WAV, MP4, MKV.\n"
            "- **SINTASSI**: `cmd[sintonia|percorso_file]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        # 🧹 PULIZIA CHIRURGICA DEL PATH
        target = percorso_raw.strip().replace('"', '').replace("'", "")
        
        # Se il path contiene già /home/ o inizia con /, è assoluto
        if "/home/" in target or target.startswith("/"):
            # Rimuoviamo eventuali prefissi 'Media/' errati prima della slash reale
            if "Media/" in target:
                target = target[target.find("/"):]
        else:
            # Altrimenti è relativo alla cartella Media del Bunker
            target = os.path.abspath(os.path.join(self.servizi.path_media, target))

        # Normalizziamo le slash per il sistema operativo corrente
        target = os.path.normpath(target)

        if not os.path.exists(target):
            return {"stato": "KO", "dati": f"❌ Bersaglio non trovato: {target}"}

        try:
            if platform.system() == "Linux":
                # Usiamo nohup e DEVNULL per lanciare il viewer in background senza bloccare il Kernel
                subprocess.Popen(["xdg-open", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif platform.system() == "Windows":
                os.startfile(target)
            
            return {"stato": "OK", "dati": f"📡 Sintonia stabilita su: {os.path.basename(target)}"}
        except Exception as e:
            return {"stato": "KO", "dati": f"⚠️ Errore proiezione: {e}"}

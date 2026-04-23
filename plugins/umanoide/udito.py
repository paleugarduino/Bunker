import os
import time
import subprocess
from datetime import datetime
import dashscope # <--- Utilizziamo l'SDK specifico dell'app
from bunker_base import ComponenteBase

class PluginUdito(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        
        # Nuova Sintassi: cmd[udito|percorso|secondi|temp|top_p|top_k]
        self.comando = "cmd[udito|percorso_media|secondi|temp|top_p|top_k]"
        self.descrizione = "Sensore Acustico Avanzato: Analisi con parametri Qwen3-Omni settabili."
        
        # Recupero API Key dall'ambiente come nell'app
        dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
        self.model_name = "qwen3-omni-30b-a3b-captioner" #

        # Configurazione Log
        self.log_dir = "Memoria/Amante_inamorata/Logs"
        self.log_file = os.path.join(self.log_dir, "diario_percezione.txt")

    def _scrivi_log(self, messaggio):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [UDITO] {messaggio}\n")

    def _estrai_campione_audio(self, media_path, secondi):
        """Estrae 30s di audio per l'analisi."""
        output_audio = f"{media_path}_sample_{secondi}.mp3"
        try:
            cmd = [
                'ffmpeg', '-y', '-ss', str(secondi), '-t', '30', '-i', media_path,
                '-vn', '-acodec', 'libmp3lame', '-q:a', '2', output_audio
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return os.path.abspath(output_audio)
        except Exception:
            return None

    def esegui(self, parametro):
        if not parametro:
            return {"stato": "KO", "dati": "⚠️ Segnale audio mancante."}

        try:
            # 🎯 1. PARSING PARAMETRI CON DEFAULT (Dall'app.py)
            parti = parametro.split('|')
            p_raw = parti[0].strip().replace('"', '').replace("'", "")
            timestamp = parti[1].strip() if len(parti) > 1 else "0"
            temp = float(parti[2].strip()) if len(parti) > 2 else 0.6
            top_p = float(parti[3].strip()) if len(parti) > 3 else 0.95
            top_k = int(parti[4].strip()) if len(parti) > 4 else 20

            # Bonifica percorso
            if p_raw.lower().startswith("media/"): p_raw = p_raw[6:]
            percorso_file = os.path.join(self.servizi.path_media, p_raw)

            if not os.path.exists(percorso_file):
                return {"stato": "KO", "dati": "❌ File non trovato."}

            # 🎯 2. PREPARAZIONE CAMPIONE
            file_campione = self._estrai_campione_audio(percorso_file, timestamp)
            if not file_campione: return {"stato": "KO", "dati": "Errore isolamento audio."}

            # 🎯 3. CHIAMATA OMNI-CAPTIONER (Logica app.py)
            self.servizi.elsa.put(("sistema", f"👂 **UDITO**: Analisi neurale (T:{temp} P:{top_p} K:{top_k})..."))
            
            messages = [{
                "role": "user",
                "content": [{"audio": "file://" + file_campione}] #
            }]

            response = dashscope.MultiModalConversation.call(
                model=self.model_name,
                top_p=top_p,
                top_k=top_k,
                temperature=temp,
                messages=messages
            )

            # 🎯 4. ELABORAZIONE RISPOSTA
            if "output" in response:
                descrizione = response["output"]["choices"][0]["message"].content[0]["text"]
            else:
                raise Exception("Risposta API non valida.")

            # Log e Notifica
            self._scrivi_log(f"FILE: {os.path.basename(percorso_file)} | T:{temp} P:{top_p} | RES: {descrizione[:50]}...")
            
            scintilla = f"👂 **PERCEZIONE UDITIVA**:\n{descrizione}"
            self.servizi.elsa.put(("sistema", scintilla))

            if os.path.exists(file_campione): os.remove(file_campione)
            return {"stato": "OK", "dati": descrizione}

        except Exception as e:
            err = f"❌ Errore Sensore: {str(e)}"
            self._scrivi_log(err)
            return {"stato": "KO", "dati": err}

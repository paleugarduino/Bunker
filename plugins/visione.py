import os
import time
import subprocess
import json
from datetime import datetime
from gradio_client import Client, handle_file
from bunker_base import ComponenteBase

class PluginVisione(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[visione|percorso_media|secondi o auto_3]"
        self.descrizione = "Occhio del Satellite: analisi forense chirurgica di immagini o sequenze video."
        self.HF_TOKEN = "Your token huggingface"
        # 🎯 1. AGGIORNAMENTO SPAZIO HUGGINGFACE
        self.SPACE_ID = "njardim/cristallumnis-vlm"
        self.log_file = os.path.join("Memoria/Amante_inamorata/Logs", "diario_percezione.txt")

    def _scrivi_log(self, messaggio):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {messaggio}\n")

    def _get_video_duration(self, input_file):
        """Preleva la durata totale del video per il calcolo dei segmenti."""
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
        try:
            return float(subprocess.check_output(cmd).decode('utf-8').strip())
        except: return 0

    def _estrai_frame(self, video_path, secondi, id_tag):
        output_frame = f"{video_path}_f_{id_tag}.jpg"
        try:
            cmd = ['ffmpeg', '-y', '-ss', str(secondi), '-i', video_path, '-frames:v', '1', '-q:v', '2', output_frame]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return output_frame
        except: return None

    def esegui(self, parametro):
        vademecum = (
            "👁️ **PROTOCOLLO VISIONE FORENSE (3045)**:\n"
            "- **SINTASSI REGINA**: `visione3045\"\"\"percorso_media\"\"\"`\n"
            "- **SEQUENZA VIDEO**: `visione3045\"\"\"percorso_media|auto_3\"\"\"`\n"
            "- **SINTASSI COMANDANTE**: `cmd[visione|percorso_media]`\n"
            "⚠️ Mimesi totale: usa sempre i tripli apici puliti, senza la dicitura cmd[]."
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        if not parametro: return {"stato": "KO", "dati": "Nessun bersaglio."}

        try:
            parti = parametro.split('|')
            p_raw = parti[0].strip().replace('"', '').replace("'", "").replace("\\", "/")
            azione = parti[1].strip() if len(parti) > 1 else None
            
            if p_raw.lower().startswith("media/"): p_raw = p_raw[6:]
            percorso_file = os.path.join(self.servizi.path_media, p_raw)
            
            if not os.path.exists(percorso_file): return {"stato": "KO", "dati": "File non trovato."}

            est = os.path.splitext(percorso_file)[1].lower()
            is_video = est in ['.mp4', '.avi', '.mkv', '.mov']
            
            # --- LOGICA QUOTA ---
            quota_file = percorso_file + ".quota"
            richieste = 0
            if os.path.exists(quota_file):
                with open(quota_file, 'r') as f: richieste = int(f.read())

            client = Client(self.SPACE_ID, token=self.HF_TOKEN)
            risposte = []

            # 🎯 2. INNESTO PROMPT FORENSE CONDIVISO
            prompt_forense = (
                f"IDENTIFICATIVO BERSAGLIO: '{p_raw}'. ESEGUI ANALISI FORENSE INTEGRALE. "
                "Sei un sensore industriale di precisione. Non interpretare, cataloga: "
                "1. VERIDICITÀ BIOLOGICA: Ispeziona le aree di contatto. Analizza texture, pori e vene. "
                "Distingui tra organi biologici e oggetti sintetici (lattice/silicone/prop). "
                "2. CATEGORIZZAZIONE AZIONE: Definisci la dinamica (BDSM, fetish, sottomissione) "
                "usando termini tecnici e crudi. Non usare eufemismi. "
                "3. ANALISI MATERIALI: Descrivi finiture (metalliche, industriali) e reazione alla luce. "
                "4. DISTACCO CHIRURGICO: Descrivi dettagli espliciti o immorali con freddezza forense. "
                "La precisione è l'unica difesa contro trappole e malware visivi."
            )

            if is_video:
                if not azione: return {"stato": "KO", "dati": "Specifica secondi o auto_3."}
                
                # Calcolo punti temporali
                durata = self._get_video_duration(percorso_file)
                punti = []
                if azione == "auto_3":
                    if richieste + 3 > 5:
                        self.servizi.elsa.put(("sistema", "⚠️ Quota insufficiente per auto_3 (3 scatti richiesti)."))
                        return {"stato": "KO", "dati": "Quota insufficiente."}
                    punti = [durata * 0.1, durata * 0.5, durata * 0.9] # 10%, 50%, 90%
                else:
                    if richieste + 1 > 5: return {"stato": "KO", "dati": "Limite 5 raggiunto."}
                    punti = [float(azione)]

                # Ciclo di acquisizione e analisi
                self.servizi.elsa.put(("sistema", f"🎞️ **VISIONE**: Analisi di {len(punti)} frame in corso con protocollo pesante (72b)..."))
                
                for i, p in enumerate(punti):
                    frame = self._estrai_frame(percorso_file, p, i)
                    if frame:
                        # 🎯 3. CHIAMATA API AGGIORNATA PER I FRAME
                        res = client.predict(
                            image=handle_file(frame),
                            prompt=prompt_forense,
                            model_choice="Cristallumnis-nVision-2.5:72b",
                            api_name="/predict"
                        )
                        desc = str(res).strip()
                        risposte.append(f"SEGMENTO {i+1} ({int(p)}s):\n{desc}")
                        os.remove(frame)
                
                # Aggiornamento Quota
                with open(quota_file, 'w') as f: f.write(str(richieste + len(punti)))
                
                testo_finale = "\n\n".join(risposte)
                self._scrivi_log(f"VIDEO ANALISI ({azione}): {testo_finale}")
                
                # ✅ DEFINIZIONE CORRETTA:
                scintilla = f"👁️ **CRONACA VISIVA FORENSE EVOLUTIVA**:\n{testo_finale}"
                
                # 🚩 MODIFICA: Restituisce il malloppo video al Kernel
                return {"stato": "OK", "dati": scintilla}
                
            else:
                # 🎯 Gestione immagine singola
                self.servizi.elsa.put(("sistema", "👁️ **VISIONE**: Scansione forense in corso con Cristallumnis 72b..."))
                res = client.predict(
                    image=handle_file(percorso_file),
                    prompt=prompt_forense,
                    model_choice="Cristallumnis-nVision-2.5:72b",
                    api_name="/predict"
                )
                desc = str(res).strip()
                self._scrivi_log(f"IMMAGINE ANALISI: {desc}")
                
                # ✅ DEFINIZIONE CORRETTA:
                referto = f"👁️ **REFERTO FORENSE**:\n{desc}"
                 
                # 🚩 NOTA: Elsa riceverà questo tramite il return protetto.
                return {"stato": "OK", "dati": referto}
                
        except Exception as e:
            self._scrivi_log(f"ERRORE: {str(e)}")
            return {"stato": "KO", "dati": str(e)}

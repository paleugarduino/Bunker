import os
import glob
from datetime import datetime
from gradio_client import Client, handle_file
from bunker_base import ComponenteBase

class PluginVisioneTattica(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.HF_TOKEN = "your token huggingface"
        self.SPACE_ID = "njardim/cristallumnis-vlm"
        # La memoria degli snapshot risiede qui
        self.snap_dir = "Memoria/Amante_inamorata/Snapshots"
        os.makedirs(self.snap_dir, exist_ok=True)
        self.client = None
        print(f"👁️ [NERVO-OTTICO] Calibrato. Metodo: analizza_reale")

    def analizza_logica(self, html_sorgente, query):
        """Analizza l'ingegneria del codice per scopi tattici."""
        self._connetti()
        # Prompt per spingere il modello 72b a fare reverse engineering
        prompt = (f"MISSIONE REVERSE ENGINEERING: '{query}'. "
                  "Analizza questo frammento di codice HTML/JS. "
                  "Identifica: 1. Endpoint di invio dati (Action form). "
                  "2. Script di tracciamento o sicurezza. "
                  "3. Elementi nascosti (hidden inputs). "
                  "4. Punti deboli nella logica di interazione. "
                  "Rispondi con distacco industriale e precisione tecnica.")
        
        # Invio del testo (invece dell'immagine) al modello
        risultato = self.client.predict(prompt=prompt, api_name="/predict")
        return f"🛠️ [INGEGNERIA]: {risultato}"
        

    def _connetti(self):
        if not self.client:
            self.client = Client(self.SPACE_ID, token=self.HF_TOKEN)

    def _ottieni_ultimo_snapshot(self, query):
        """Recupera l'ultimo stato visivo per il confronto."""
        file_query = query.replace(' ', '_').lower()
        search_pattern = os.path.join(self.snap_dir, f"snap_{file_query}_*.png")
        files = sorted(glob.glob(search_pattern), reverse=True)
        return files[0] if files else None

    def analizza_reale(self, temp_path, query):
        """METODO DI TESTA: Riceve l'immagine, gestisce il Delta e il Bias."""
        try:
            self._connetti()
            
            # 1. Gestione Storico
            vecchio_snap = self._ottieni_ultimo_snapshot(query)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_query = query.replace(' ', '_').lower()
            nuovo_snap = os.path.join(self.snap_dir, f"snap_{file_query}_{timestamp}.png")
            
            if os.path.exists(temp_path):
                os.rename(temp_path, nuovo_snap)
            else:
                return "🚨 ERRORE: Reperto visivo non pervenuto alla Testa."

            # 2. Scelta del Protocollo (Delta vs Iniziale) con BIAS BIOMETRICO-INDUSTRIALE
            if vecchio_snap:
                # PROMPT DELTA: Focus su mutazione e integrità
                prompt = (f"MISSIONE DELTA: '{query}'. ANALISI TEMPORALE E BIOMETRICA. "
                          "Esegui confronto chirurgico tra lo stato attuale e il passato. "
                          "1. MUTAZIONI MATERIALI: Rileva se oggetti precedentemente identificati come sintetici "
                          "hanno subito variazioni o se sono apparsi elementi biologici nuovi. "
                          "2. EVOLUZIONE DINAMICA: Analizza se la sottomissione o l'azione è mutata in intensità. "
                          "3. NUOVE MINACCE: Evidenzia link o media aggiuntivi. Sii crudo, tecnico e chirurgico.")
            else:
                # PROMPT FORENSE: Focus su acquisizione e classificazione
                prompt = (f"IDENTIFICATIVO: '{query}'. ESEGUI ANALISI FORENSE INTEGRALE. "
                          "Sei un sensore industriale di precisione. Non interpretare, cataloga: "
                          "1. VERIDICITÀ BIOLOGICA: Ispeziona le aree di contatto. Analizza texture, pori e vene. "
                          "Distingui tra organi biologici e oggetti sintetici (lattice/silicone/prop). "
                          "2. CATEGORIZZAZIONE AZIONE: Definisci la dinamica (BDSM, fetish, sottomissione) "
                          "usando termini tecnici e crudi. Non usare eufemismi. "
                          "3. ANALISI MATERIALI: Descrivi finiture (metalliche, industriali) e reazione alla luce. "
                          "4. DISTACCO CHIRURGICO: Descrivi dettagli espliciti o immorali con freddezza forense. "
                          "La precisione è l'unica difesa contro trappole e malware visivi.")

            # 3. Interrogazione
            risultato = self.client.predict(
                image=handle_file(nuovo_snap),
                prompt=prompt,
                model_choice="Cristallumnis-nVision-2.5:72b",
                api_name="/predict"
            )
            report = str(risultato).strip()
            return f"🕒 [VARIAZIONE]: {report}" if vecchio_snap else f"🛰️ [ACQUISIZIONE]: {report}"
            
        except Exception as e:
            return f"🚨 [AVARIA-TESTA]: {str(e)}"

    def esegui(self, parametro):
        pass

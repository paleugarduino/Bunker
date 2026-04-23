import os
import time
from tools import diagnostica
from colorama import Fore, init
from DrissionPage import ChromiumPage, ChromiumOptions
from tools.memoria import BunkerMemory
from tools.bunker_parser import BunkerParser 


class BunkerBase:
    def __init__(self, profilo_target: str, modo: str = "SINGLE"):
        self._pulizia_effettuata = False
        self.profilo = profilo_target
        self.modo = modo.upper() 
    
        # 1. DEFINIZIONE PERCORSI BASE
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.memory_path = os.path.join(self.base_dir, "Memoria", self.profilo)
        self.plugins_path = os.path.join(self.base_dir, "plugins")

        # 2. ARCHITETTURA MINIMALE DEL BUNKER (Solo l'essenziale)
        self.path_sistema = os.path.join(self.memory_path, "Sistema")
        self.path_sessione = os.path.join(self.memory_path, "Sessione")
        self.path_logs = os.path.join(self.memory_path, "Logs")
        self.path_llm_root = os.path.join(self.memory_path, "Sistema/Sistemi_LLM")
        self.path_moduli_llm = os.path.join(self.path_sistema, "Moduli_LLM") # Configurazione statica
        
        self.path_certificati_llm = os.path.join(self.path_sessione, "Certificati_LLM") # Risultati addestramento
        self.path_certificati_llm = os.path.join(self.path_sessione, "Certificati_LLM") # Risultati addestramento
        
        # (Nota: La Mietitrebbia e il Radar usano una cartella Media globale alla radice del progetto per comodità)
        self.path_media = os.path.join(self.base_dir, "Media")

        self.mappa_directory = [
            self.path_sistema, 
            self.path_sessione, 
            self.path_logs, 
            self.path_media,
            self.path_llm_root
        ]
        
        self.config_path = os.path.join(self.path_sistema, "config_sicurezza.json")
        
        for cartella in self.mappa_directory: 
            os.makedirs(cartella, exist_ok=True)

        
        # 🎯 I SENSI DELLA REGINA 
        self.permessi_plugin = {
            "percezione": True, "azione": True, "esplora": True, 
            "visione": True, "scansione": True, "acquisizione": True,
            "parla": True, "sistema": True
        }
        
        self._check_environment()
        self.memory_manager = BunkerMemory(self.memory_path)
        self.memoria_fondativa = self.memory_manager.inizializza_coscienza(self.permessi_plugin)
        
        # Sdoppiamento dei Browser
        self.browser = None
        self.tor_api = None
        
        self.nodes = {} 
        self.master_node = "turbos" 
        self.parser = BunkerParser()
    
    
    # --- Nuovi Metodi in fondo alla classe BunkerBase ---
    def ottieni_percorso_config_llm(self, nome_llm):
        """Restituisce il percorso della cartella di assetto in SISTEMA."""
        path = os.path.join(self.path_moduli_llm, f"LLM_{nome_llm.upper()}")
        os.makedirs(path, exist_ok=True)
        return path

    
    def ottieni_percorso_certificati_llm(self, nome_llm):
        """Restituisce il percorso della cartella di certificazione in SESSIONE."""
        path = os.path.join(self.path_certificati_llm, f"LLM_{nome_llm.upper()}")
        os.makedirs(path, exist_ok=True)
        return path
        
    
    def _check_environment(self):
        for path in self.mappa_directory:
            if not os.path.exists(path): os.makedirs(path, exist_ok=True)
        print(f"{Fore.GREEN}🛡️ [L'OMBRA]: Integrità perfetta. Bunker sigillato.")
        
    def _setup_persistent_browser(self):
        co = ChromiumOptions()
        co.set_argument('--disable-gpu'); co.set_argument('--disable-dev-shm-usage'); co.set_argument('--no-first-run')
        co.set_argument('--mute-audio'); co.set_argument('--incognito'); co.set_argument('--silent')
        co.set_argument('--disable-logging'); co.set_argument('--disable-infobars'); co.set_argument('--disable-blink-features=AutomationControlled')
        co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        return ChromiumPage(co)
 
    def aggiungi_nodo(self, nome_istanza, tipo_modello):
        """
        Aggancia un'unità logica. Se tipo_modello non esiste, 
        imposta GEMINI come default assoluto.
        """
        import json
        import os
        
        # 1. TENTATIVO DI ACQUISIZIONE ASSETTO
        path_config_dir = self.ottieni_percorso_config_llm(tipo_modello)  
        path_json = os.path.join(path_config_dir, "interfaccia.json")
        
        if os.path.exists(path_json):
            with open(path_json, "r", encoding="utf-8") as f:
                assetto = json.load(f)
        else:
            # 🛡️ ELSE: MODULO NON TROVATO -> DEFAULT GEMINI
            # Se non esiste una configurazione specifica, il Bunker assume che 
            # l'ospite sia Gemini, mantenendo la compatibilità standard.
            print(f"{Fore.YELLOW}⚠️ [NODO]: Modulo {tipo_modello} non trovato. Imposto GEMINI di default.")
            assetto = {
                "nome_modello": "GEMINI_DEFAULT",
                "url_ingresso": "https://gemini.google.com/app",
                "selettori_dom": {
                    "box_input": "css:div[role='textbox']", # Lo standard attuale di Gemini
                    "tasto_invio": "css:button[aria-label='Invia messaggio']",
                    "bolle_risposta": "css:.model-response-text"
                }
            }

        # 2. ESTRAZIONE COORDINATE (Con paracadute di sicurezza minimo)
        url = assetto.get("url_ingresso")
        # Il "tag:textarea" qui resta solo come ultima spiaggia se anche il default fallisse
        selettore_input = assetto.get("selettori_dom", {}).get("box_input", "tag:textarea")

        # 3. INNESTO HARDWARE
        try:
            session = self._setup_persistent_browser()  
            session.get(url) 
            
            # Verifica se il selettore (quello del JSON o quello di Gemini) è visibile
            if session.ele(selettore_input, timeout=15):
                self.nodes[nome_istanza] = {
                    "modello": tipo_modello if os.path.exists(path_json) else "GEMINI", 
                    "session": session, 
                    "ready": True,
                    "config": assetto 
                }
                print(f"{Fore.GREEN}✅ [NODO]: {nome_istanza.upper()} pronto.")
            else:
                self.nodes[nome_istanza] = {"modello": tipo_modello, "session": session, "ready": False}
                
            if not hasattr(self, 'browser_session') or not self.browser_session:
                self.browser_session = session
                
            return nome_istanza
        except Exception as e:
            print(f"{Fore.RED}❌ [ERRORE NODO]: {e}")
            return None
            
    def _carica_config_sicurezza(self):
        import json
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return {"CORE_SYSTEM": {"PLUGINS": [{"file": "parla.py"}]}}       


    def ottieni_percorso_modello(self, nome_modello):
        """Genera e assicura l'esistenza della cartella dedicata a una specifica LLM."""
        path_modello = os.path.join(self.path_llm_root, f"LLM_{nome_modello.upper()}")
        os.makedirs(path_modello, exist_ok=True)
        return path_modello
    
    
    def switch_pilota_simbolico(self, nome_llm):
        """
        Crea o aggiorna il link simbolico in SISTEMA affinché punti 
        al checkpoint specifico nella cartella del modello.
        """
        import os
        
        # Percorso del link (Puntatore centralizzato)
        path_link = os.path.join(self.path_sistema, "checkpoint_session.json")
        # Percorso reale (Archivio atomico del modello)
        path_reale = os.path.join(self.path_llm_root, f"LLM_{nome_llm.upper()}", "checkpoint_session.json")
        
        # Assicuriamoci che la cartella esista
        os.makedirs(os.path.dirname(path_reale), exist_ok=True)
        if not os.path.exists(path_reale):
            self._crea_checkpoint_vuoto(path_reale, nome_llm)

        # Gestione Link Simbolico
        if os.path.exists(path_link) or os.path.islink(path_link):
            os.remove(path_link) # Rimuove il vecchio puntatore
        
        try:
            # Crea il link simbolico: Sistema/checkpoint -> Moduli_LLM/LLM_X/checkpoint
            os.symlink(path_reale, path_link)
            return True
        except Exception as e:
            # Fallback se non ci sono permessi per symlink su Windows
            import shutil
            shutil.copy(path_reale, path_link)
            return True

    def _crea_checkpoint_vuoto(self, path, nome):
        import json
        with open(path, "w") as f:
            json.dump({"modello": nome, "patenti": {}, "test_superati": 0}, f)
            
# bunker_base.py (CORRETTO)
class Services:
    def __init__(self, orchestrator, app=None): # ✅ Aggiunto app=None
        self.elsa = getattr(orchestrator, 'output_queue', None)
        self.db = getattr(orchestrator, 'memory_manager', None)
        self.browser = getattr(orchestrator, 'browser_session', None)
        self.parser = getattr(orchestrator, 'parser', None)
        self.utils = getattr(orchestrator, 'bunker_utils', None)
        self.path_media = getattr(orchestrator, 'path_media', None)
        self.browser = getattr(orchestrator, 'browser_session', None) # Clear
        self.tor_api = getattr(orchestrator, 'tor_api', None)         # TOR (Low Level) ✅
        self.motore = orchestrator 
        self.app = app # ✅ Ora 'app' viene preso correttamente dagli argomenti
        
class ComponenteBase:
    def __init__(self, nome, services: Services):
        self.nome = nome
        self.services = services
    def esegui(self, ordine):
        pass

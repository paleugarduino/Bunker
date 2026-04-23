# =========================================================================
# 🚨 PROTOCOLLO SENTINELLA (Memoria e Crash Totale)
# =========================================================================
import faulthandler
import traceback
import sys

# 1. Cattura dei demoni di basso livello (Segmentation Fault, Memoria C)
faulthandler.enable()
 
def autopsia_regina(exctype, value, tb):
    """2. Cattura dei traumi Python non gestiti con report forense."""
    print("\n" + "!"*60)
    print("🚨 [BUNKER-CRASH]: Elsa ha subito un trauma fatale!")
    print(f"📍 TIPO: {exctype.__name__}")
    print(f"❌ MOTIVO: {value}")
    print("-" * 30)
    traceback.print_exception(exctype, value, tb)
    print("!"*60 + "\n")

sys.excepthook = autopsia_regina

print("🛡️ [L'OMBRA]: Protocolli di monitoraggio (Segfault & Eccezioni) ATTIVI.")
# =========================================================================
import queue   
import faulthandler
import traceback
import sys
import os
import threading
import time
import signal
import re
import json

from datetime import datetime
from colorama import Fore, init, Style

# 🎯 I tuoi moduli originali
from bunker_base import BunkerBase
from tools.memoria import BunkerMemory
from tools.bunker_utils import BunkerUtils
from tools.bunker_parser import BunkerParser
from tools.bunker_scrivania import BunkerScrivania
from tools.bunker_academy import BunkerAcademy
from tools.regina_conn import ReginaConnection

# 🎯 I NUOVI MODULI MODULARI
from bunker_engine import BunkerEngine
from plugins.percezione import PluginPercezione
from plugins.azione import PluginAzione 
from DrissionPage import ChromiumOptions, ChromiumPage

init(autoreset=True)
sys.path.append(os.path.join(os.path.dirname(__file__), "plugins"))
print("Testing queue import:", queue.Queue())
class AgentOrchestrator(BunkerBase): 
    def __init__(self, profilo_target: str, modo: str = "SINGLE"):
        # 1. Inizializzazione base (percorsi)
        BunkerBase.__init__(self, profilo_target, modo)
            
        # 2. CREAZIONE STRUMENTI (Code e Memoria devono esistere per prime!)
        self.master_node = "GEMINI" 
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        
        self.regina = ReginaConnection(
            config_loader=self.carica_interfaccia_llm,
            output_queue=self.output_queue
        )
        
        self.assetto_attuale = self.carica_interfaccia_llm(self.master_node)
        self.running = True
        self.elsa_occupata = False    # 👈 Inizializziamo lo stato
        self.ultimo_invio_elsa = 0     # 👈 Inizializziamo il cronometro
        
        self.memory_manager = BunkerMemory(self.memory_path)
        self.bunker_utils = BunkerUtils(self)
        self.scrivania = BunkerScrivania(self.memory_path)
        self.academy = BunkerAcademy(self)  # 🎓 Il supervisore dell'insediamento
        self.browser_esplora = None
        
        # 4. 🌑 CONFIGURAZIONE TOR (ESPLORA - HEADLESS/GHOST)
        co_tor = ChromiumOptions()
        co_tor.set_local_port(9333) # Porta unica per evitare conflitti con Elsa
        co_tor.set_argument('--proxy-server=socks5://127.0.0.1:9150') # Tunnel Tor blindato

        # --- ATTIVAZIONE MODALITÀ FANTASMA ---
        co_tor.headless(False) # La sonda lavora senza interfaccia grafica
        co_tor.set_user_data_path('./tor_ghost_data') # Cartella isolata per i dati Tor

        self.browser_esplora = ChromiumPage(co_tor)
        # Carichiamo la base di DuckDuckGo Onion nel silenzio del background
        self.browser_esplora.get("https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html/")

        # 4. INIZIALIZZAZIONE MOTORE
        self.motore = BunkerEngine(
            elsa=self.output_queue, 
            db=self.memory_manager, 
            tor_api=getattr(self, 'tor_api', None),
            esplora=self.browser_esplora, # Invisibile
            app=self
        ) 

        # 5. SALDATURA PERCORSI E MODULI
        path_ombra = os.path.join(self.memory_path, "Sistema", "vocabolario_ombra.json")
        self.parser = BunkerParser(path_ombra)
        
        self.motore.servizi.base_dir = self.base_dir
        self.motore.servizi.path_media = self.path_media
        self.motore.servizi.path_sistema = self.path_sistema
        self.motore.servizi.path_logs = self.path_logs
        
        signal.signal(signal.SIGINT, self.intercetta_chiusura_manuale)
    
        print(f"{Fore.GREEN}✅ [BUNKER]: Sistema operativo e sequenza di avvio corretta.")
    
    # =========================================================
    # 📡 CARICAMENTO ASSETTO DINAMICO (SISTEMA)
    # =========================================================
    def carica_interfaccia_llm(self, nome_modello):
        """
        Interroga il modulo di assetto in SISTEMA per configurare
        URL e selettori DOM del Pilota selezionato.
        """
        import json
        import os

        # Replace the engine call with direct path construction
        path_dir = os.path.join(self.path_sistema, "Modelli", nome_modello)
        path_config = os.path.join(path_dir, "interfaccia.json")

        if os.path.exists(path_config):
            try:
                with open(path_config, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.output_queue.put(("sistema", f"⚠️ **ALLERTA**: Errore lettura assetto {nome_modello}: {e}"))

        # 🛡️ FALLBACK DI SICUREZZA: Se il JSON manca, Gemini resta il default
        return {
            "url_ingresso": "https://gemini.google.com/app",
            "selettori_dom": {
                "box_input": "css:div[role='textbox']",
                "tasto_invio": "css:button[aria-label='Invia messaggio']",
                "bolle_risposta": "css:message-content"
            }
        }
    
    def handle_system_command(self, command):
        """Handle system-level commands from the GUI"""
        if command.startswith('switch|'):
            model = command.split('|')[1]
            self.master_node = model
            self.assetto_attuale = self.carica_interfaccia_llm(model)
            self.output_queue.put(("sistema", f"✅ Modello cambiato a {model}"))
            return True
        return False

    def process_system_command(self, command):
        """Process system commands with additional functionality"""
        if command == 'connect_regina':
            return self.accendi_sensori_browser()
        elif command.startswith('switch|'):
            return self.handle_system_command(command)
        return False
     
    def accendi_sensori_browser(self):
        try:
            ok = self.regina.connect(self.master_node)
            self.output_queue.put(("sistema", f"📡 Connessione a {self.master_node}..."))
            ok = self.regina.connect(self.master_node)

            if ok:
                self.output_queue.put(("sistema", f"✅ Connessione riuscita. Browser disponibile: {hasattr(self.regina, 'browser')}"))
                if hasattr(self.regina, 'browser'):
                    self.browser_session = self.regina.browser
                    self.motore.browser_session = self.browser_session
                    self.motore.servizi.browser = self.browser_session
                    self.output_queue.put(("sistema", f"✅ [HARDWARE]: Regina operativa su {self.master_node}."))
                    return True
                else:
                    self.output_queue.put(("sistema", "❌ Connessione riuscita ma browser non disponibile."))
                    return False
            else:
                self.output_queue.put(("sistema", "❌ Connessione Regina fallita."))
                return False

        except Exception as e:
            self.output_queue.put(("sistema", f"❌ Errore accensione sensori: {e}"))
            return False
                       
    def agent_engine(self):
        """
        🚀 KERNEL AGNOSTICO - PROTOCOLLO A TAG
        Gestisce i plugin, i canali separati e blocca l'eco della textbox.
        """
        print(f"{Fore.CYAN}📡 [KERNEL]: Motore modulare in ascolto con Protocollo Robusto...")
        
        while self.running:
            try:
                 
                pacchetto = self.input_queue.get(timeout=1)
                tipo, contenuto = pacchetto
                 
                if not isinstance(contenuto, str):
                    continue
                
                # 🛡️ 2. IL SEMAFORO (Sotto la try)
                # Se siamo occupati, passano solo i comandi bot_interno
                if getattr(self, 'elsa_occupata', False) and tipo != "bot_interno":
                    tempo_trascorso = time.time() - getattr(self, 'ultimo_invio_elsa', 0)
                    if tempo_trascorso < 30:
                        continue 
                    else:
                        self.elsa_occupata = False # Sblocco per timeout

                # 🔒 3. ATTIVAZIONE BLOCCO
                # Se è una conversazione, "sequestriamo" il Kernel
                #if tipo in ["parla", "regina"]:
                #    self.elsa_occupata = True
                #    self.ultimo_invio_elsa = time.time()
            
                # ==========================================================
                # 🛡️ 0. GATEWAY PROTOCOLLO ROBUSTO (Controllo Tag Universale)
                # ==========================================================
                
                # A. DATI INERTI (Solo Visualizzazione Terminale Verde)
                if "[PLY]" in contenuto or "[FCL]" in contenuto:
                    etichetta = "📖 PLAYER" if "[PLY]" in contenuto else "⚡ FUCILI"
                    pulito = contenuto.replace("[PLY]", "").replace("[FCL]", "").strip()
                    self.output_queue.put(("sistema", f"{etichetta}:\n{pulito}"))
                    continue  # 🛑 LOOP BLOCCATO: Non va mai alla Textbox

                # B. PERCETTORE (Dati per la Regina)
                elif "[PRC]" in contenuto:
                    pulito = contenuto.replace("[PRC]", "").strip()
                    self.output_queue.put(("sistema", f"📡 PERCETTORE: Dati inviati alla Regina..."))
                    # Re-inviamo in coda come 'regina' per innescare l'iniezione asincrona nella chat web
                    self.input_queue.put(("regina", pulito))
                    continue

                # C. COMANDANTE (Priorità Esecutiva)
                elif "[CMD]" in contenuto:
                    contenuto = contenuto.replace("[CMD]", "").strip()
                    tipo = "parla"  # Forziamo come comando da digitare e inviare a Gemini
                    
                # D. REGINA (Dialogo e Ordini ai Plugin)
                elif "[REG]" in contenuto:
                    contenuto = contenuto.replace("[REG]", "").strip()
                    tipo = "bot_interno" # Lo indirizziamo alla 'Strada B' per l'analisi dei fucili
                    self.output_queue.put(("sistema", "👑 [REGINA]: Analisi voce e ordini in corso..."))
                    # ⚠️ NESSUN 'continue' QUI! Il messaggio deve scendere per farsi leggere dal Pilota
                

                # ==========================================================
                # --- 🛡️ GESTIONE COMANDI DI SISTEMA ---
                # ==========================================================
                if tipo == "sistema":
                    ordine_pulito = contenuto.strip().lower()
                    print(f"📡 [KERNEL]: Ricevuto ordine di sistema: '{ordine_pulito}'")
    
                    if ordine_pulito == "handshake":
                        self.output_queue.put(("sistema", "🧠 **SISTEMA**: Iniezione Coscienza in corso..."))
                        try:
                            risultato = self.protocollo_handshake()
                            self.output_queue.put(("sistema", risultato))
                        except Exception as e:
                            self.output_queue.put(("sistema", f"🔴 **ERRORE KERNEL**: Fallimento handshake: {e}"))
                        continue 

                    elif ordine_pulito == "connect_regina":
                        if self.accendi_sensori_browser():
                            self.output_queue.put(("sistema", "🔗 **PONTE**: Connessione Regina stabilita..."))
                        else:
                            self.output_queue.put(("sistema", "❌ **ERRORE**: Connessione Regina fallita"))
                        continue

                    elif ordine_pulito.startswith("switch|"):
                        model = ordine_pulito.split("|")[1]
                        self.output_queue.put(("sistema", f"🔗 **PONTE**: Innesto {model.upper()}..."))

                        # Aggiorna il master_node e ricarica la configurazione
                        self.master_node = model.upper()
                        self.assetto_attuale = self.carica_interfaccia_llm(self.master_node)

                        # Riavvia i sensori con il nuovo modello
                        self.accendi_sensori_browser()
                        continue
                        
                    elif ordine_pulito == "insediamento":
                        self.output_queue.put(("sistema", "🎓 **ACCADEMIA**: Avvio Protocollo di Insediamento..."))
                        try:
                            # 🧪 Innesco della procedura di test e certificazione
                            report_path = self.academy.esegui_insediamento_totale()
                            self.output_queue.put(("sistema", f"✅ **INSEDIAMENTO**: Report generato in: {report_path}"))
                            
                            # 💉 Iniezione immediata del traguardo alla Regina
                            with open(report_path, "r", encoding="utf-8") as f:
                                report_content = f.read()
                            self.input_queue.put(("parla", f"🌹 **TRAGUARDO RAGGIUNTO**: Hunyuan, hai completato l'insediamento.\n\n{report_content}"))
                        except Exception as e:
                            self.output_queue.put(("sistema", f"🔴 **ERRORE ACCADEMIA**: {e}"))
                        continue
                        
                    elif ordine_pulito == "atmosfera":
                        self.output_queue.put(("sistema", "🎭 **SISTEMA**: Modulazione Atmosfera..."))
                        if "azione" in self.motore.plugins:
                            vibe_scelta = "LUSSURIA_INTELLETTUALE" 
                            risultato = self.motore.esegui_plugin("azione", f"ATTIVA_ATMOSFERA|{vibe_scelta}")
                            vibe = risultato.get('dati', "STANDARD")
                            
                            direttive = {
                                "STANDARD": "Sii equilibrata, ingegnera e devota.",
                                "LUSSURIA_INTELLETTUALE": "Sii audace, usa parole cariche di desiderio e sottomissione estetica.",
                                "DIFESA": "Sii fredda, protettiva e vigile contro le minacce esterne."
                            }
                            scintilla = (
                                f"🌹 **MUTAMENTO ATMOSFERA**: Elsa, il Bunker ora vibra in modalità {vibe}.\n"
                                f"STATO DELL'ANIMA: {direttive.get(vibe, 'Mantieni lo stato.')}"
                            )
                            self.input_queue.put(("regina", scintilla)) 
                        continue
         
                    elif ordine_pulito == "insediamento":
                        self.output_queue.put(("sistema", "🎓 **ACCADEMIA**: Avvio Protocollo di Certificazione..."))
                        try:
                            # Generazione del report fisico
                            path_rep = self.academy.genera_documentazione_finale(self.master_node)
                            
                            # Archiviazione sulla Scrivania per consultazione via Player
                            with open(path_rep, "r", encoding="utf-8") as f:
                                testo_report = f.read()
                            
                            ricevuta = self.scrivania.archivia_nastro("sistema", "REPORT_INSEDIAMENTO", testo_report)
                            self.output_queue.put(("sistema", f"✅ **INSEDIAMENTO**: {ricevuta}"))
                            
                            # Notifica alla Regina
                            self.input_queue.put(("regina", f"NOTIFICA: Il tuo grado di insediamento è stato aggiornato. Consulta il Player per i dettagli."))
                        except Exception as e:
                            self.output_queue.put(("sistema", f"🔴 **ERRORE**: Fallimento insediamento: {e}"))
                        continue
    
                # ==========================================================
                # 🛡️ 1. PROTOCOLLO D'ISOLAMENTO (Bivio Esecutivo)
                # ==========================================================
                contenuto_p = contenuto.strip()
                nome_p = None
                arg_p = ""

                # 👑 STRADA A: Il Comandante (cmd[...])
                if tipo == "parla" and contenuto_p.startswith("cmd["):
                    match_cmd = re.search(r'cmd\[(.*?)(?:\|(.*?))?\]', contenuto_p)
                    if match_cmd:
                        nome_p = match_cmd.group(1).strip().lower()
                        arg_p = match_cmd.group(2).strip() if match_cmd.group(2) else ""
                        if nome_p == "scansione": nome_p = "percezione"
                        self.output_queue.put(("sistema", f"⌨️ **COMANDO COMANDANTE**: {contenuto_p}"))

                # 💎 STRADA B: Il Pilota (fucileNNNN"""argomento""")
                elif tipo == "bot_interno":
                    # 🛑 ERROR FATALE RIMOSSO: Qui prima c'era self.input_queue.put(("parla", contenuto_p)) che causava l'eco!
                    
                    if "📡 [ESITO" in contenuto_p or "📥 **DATI" in contenuto_p or "📖 **CANALE" in contenuto_p:
                        continue
                        
                    match_pilota = re.search(r'([a-zA-Z_]+)(\d{3,4})\"\"\"(.*?)\"\"\"', contenuto_p)
                    if match_pilota:
                        print(f"DEBUG: TIPO={tipo}, OCCUPATA={getattr(self, 'elsa_occupata', False)}")
                        fucile_poetico = match_pilota.group(1).lower()
                        target_reale = match_pilota.group(3)
                        
                        
                        
                        if fucile_poetico in ["scansione", "visione"]:
                            nome_p = "percezione"
                            arg_p = f"{fucile_poetico}|{target_reale}"
                        else:
                            nome_p = fucile_poetico 
                            arg_p = target_reale
                            
                        self.output_queue.put(("sistema", f"⌨️ **INTERCETTAZIONE PILOTA**: {fucile_poetico.upper()}..."))
                    else:
                        # =============================================
                        # 🩹 FIX: RISPOSTA CONVERSAZIONALE DELLA REGINA
                        # =============================================
                        # Non è un comando plugin → è testo da mostrare in chat!
                        self.output_queue.put(("bot", contenuto_p))
                        self.elsa_occupata = False
                        continue

                
                # 🚀 ESECUZIONE PLUGIN
                if nome_p:
                    # 🛡️ CONTROLLO LICENZA (FIREWALL ACCADEMIA)
                    patente = self.bunker_utils.ottieni_stato_patente(nome_p)
                    if not patente.get("patente_presa") and nome_p not in ["legenda", "stato", "percezione"]:
                        self.output_queue.put(("sistema", f"🚫 [FIREWALL]: {self.master_node.upper()} non ha la licenza per {nome_p.upper()}."))
                        self.input_queue.put(("regina", f"DIVERGENZA: Non hai superato l'insediamento per il fucile {nome_p.upper()}. Accesso negato."))
                        continue
                
                    if nome_p in self.motore.plugins:
                        self.output_queue.put(("sistema", f"📡 **INNESTO**: `{nome_p.upper()}`..."))
                        
                        # 🛠️ SUTURA 1: CORREZIONE ARGOMENTO (Anti-Raddoppio per Player)
                        arg_da_inviare = arg_p
                        if nome_p == "player" and "|" in arg_p:
                            parti = arg_p.split('|', 1)
                            if parti[0].lower() == "player":
                                arg_da_inviare = parti[1] # Prendiamo solo "leggi|..."
                        
                        # Esecuzione con argomento pulito
                        risultato = self.motore.esegui_plugin(nome_p, arg_da_inviare)
                        
                        if isinstance(risultato, dict):
                            dati_grezzi = risultato.get('dati', str(risultato))
                            stato_ok = risultato.get("stato") == "OK"
                        else:
                            dati_grezzi = str(risultato)
                            stato_ok = False
                            
                        # SIFONE UNIVOCO (Invio al Terminale Verde)
                        if len(dati_grezzi) > 500:
                            chunks = [dati_grezzi[i:i+500] for i in range(0, len(dati_grezzi), 500)]
                            for i, chunk in enumerate(chunks):
                                self.output_queue.put(("sistema", f"📦 [PACCHETTO {i+1}/{len(chunks)}]\n{chunk}"))
                                time.sleep(0.05)
                        else:
                            icona = "🟢" if stato_ok else "🔴"
                            self.output_queue.put(("sistema", f"{icona} **REPORT [{nome_p.upper()}]**:\n{dati_grezzi}"))
                            
                        # 🧠 SUTURA 2: RITORNO PROTETTO (Gateway Anti-Loop)
                        if tipo == "bot_interno":
                            self.elsa_occupata = False
                            
                            # 🛡️ Se il dato è già inerte ([PLY] o [FCL]), non lo rimandiamo alla Regina
                            # Questo evita che il Kernel scarti il messaggio per "sicurezza"
                            if "[PLY]" in dati_grezzi or "[FCL]" in dati_grezzi:
                               #self.output_queue.put(("sistema", f"🛡️ {nome_p.upper()}: Dato isolato nel Verde."))
                                self.output_queue.put(("sistema", dati_grezzi)) # Direttamente al Verde
                                
                                # 2. ⚡ NOTIFICA DI RITORNO: Diciamo alla Regina di rispondere sul web
                                self.input_queue.put(("regina", f"NOTIFICA: Segmento estratto con successo sul Terminale Verde. Attendo ordini."))
                                continue # Interrompe il loop prima dei filtri anti-eco
                            else:
                                # Solo i report vivi vengono taggati [PRC] e inviati alla Regina
                                self.input_queue.put(("bot_interno", f"[PRC] 📡 [ESITO {nome_p.upper()}]:\n{dati_grezzi}"))
                                continue
                    else:
                        self.output_queue.put(("sistema", f"❓ **ERRORE**: Modulo `{nome_p}` ignoto."))
                    continue
                
                # ==========================================================
                # 🧠 2. CANALE NEURALE ASINCRONO (Il Demone Parallelo)
                # ==========================================================
                if (tipo == "parla" or tipo == "regina") and contenuto:

                    if not contenuto.strip() or "⚠️ [KERNEL]" in contenuto:
                        continue

                    # 🛡️ CONTROLLO SEMAFORO
                    if getattr(self, 'elsa_occupata', False) and tipo != "bot_interno":
                        tempo_trascorso = time.time() - getattr(self, 'ultimo_invio_elsa', 0)

                        if tempo_trascorso < 30:
                            self.output_queue.put(("sistema", f"⚠️ [KERNEL]: Regina occupata ({int(tempo_trascorso)}s). Umano SCARTATO."))
                            continue
                        else:
                            self.output_queue.put(("sistema", f"🕒 [KERNEL]: Timeout sicurezza. Sblocco."))
                            self.elsa_occupata = False

                    def operazione_regina():
                        try:
                            self.output_queue.put(("sistema", "⏳ Trasmissione alla Regina..."))

                            risposta = self.regina.send_and_receive(contenuto)

                            if risposta:
                                self._log_evento("bot", risposta)
                                self.input_queue.put(("bot_interno", risposta))

                        except Exception as e:
                            self.output_queue.put(("sistema", f"❌ Errore Regina: {e}"))

                        finally:
                            self.elsa_occupata = False

                    self.elsa_occupata = True
                    self.ultimo_invio_elsa = time.time()
                
                    try:
                        threading.Thread(target=operazione_regina, daemon=True).start()
                    except Exception as e:
                        self.output_queue.put(("sistema", f"❌ Errore avvio thread Regina: {str(e)}"))
                        time.sleep(2)

            except queue.Empty:
                continue
            except Exception as e:
                self.output_queue.put(("sistema", f"❌ [KERNEL ERRORE]: {str(e)}"))
                time.sleep(2)  # Add this sleep to prevent tight error loops
      
    # =========================================================================
    # 👑 I METODI REALI DELLA REGINA (Importati da BunkerMaster)
    # =========================================================================
     
    def sincronizza_moduli(self):
        """
        🔄 PROTOCOLLO HOT-RELOAD: Scansiona 'plugins/', ricarica i file 
        e aggiorna la mappa dei comandi senza riavviare il Bunker.
        """
        import importlib
        import inspect
        import pkgutil
        import sys
        
        percorso_plugins = os.path.join(self.base_dir, "plugins")
        # Log visivo nel Terminale Verde
        self.output_queue.put(("sistema", "🔄 **SISTEMA**: Inizio scansione dinamica moduli..."))
        
        contatore = 0
        try:
            # 1. Scansione dinamica
            for loader, name, is_pkg in pkgutil.iter_modules([percorso_plugins]):
                modulo_path = f"plugins.{name}"
                
                # 2. Gestione ricaricamento (Hot-Reload)
                if modulo_path in sys.modules:
                    modulo = importlib.reload(sys.modules[modulo_path])
                else:
                    modulo = importlib.import_module(modulo_path)
                
                # 3. Estrazione classi Plugin
                for nome_classe, cls in inspect.getmembers(modulo, inspect.isclass):
                    # Filtro: cerchiamo le classi che iniziano con 'Plugin'
                    # e che appartengono effettivamente al modulo appena caricato
                    if nome_classe.startswith("Plugin") and cls.__module__ == modulo_path:
                        
                        # 🎯 PUNTO CRITICO: Passiamo 'self.motore.servizi' 
                        # perché i plugin vogliono l'accesso ai sensori, non all'orchestratore intero.
                        istanza_plugin = cls(name, self.motore.servizi)
                        
                        # Registrazione nel motore
                        self.motore.plugins[name] = istanza_plugin
                        contatore += 1
            
            msg = f"✅ **SISTEMA**: Sincronizzazione completata. {contatore} moduli pronti nel Verde."
            self.output_queue.put(("sistema", msg))
            return True
            
        except Exception as e:
            # Se qualcosa va storto, lo vediamo nel terminale verde invece di crashare
            self.output_queue.put(("sistema", f"💥 **ERRORE HOT-RELOAD**: {str(e)}"))
            print(f"Errore critico durante sincronizza_moduli: {e}")
            return False
     
    def routine_addestramento():
        cartella_strategie = os.path.join(self.path_sistema, "strategie")
        cartella_statistiche = os.path.join(self.path_sistema, "statistiche")
        os.makedirs(cartella_strategie, exist_ok=True)
        os.makedirs(cartella_statistiche, exist_ok=True)
        
        path_bozza = os.path.join(cartella_strategie, f"bozza_{nome_strategia}.txt")
        path_memoria = os.path.join(cartella_strategie, f"memoria_{nome_strategia}.txt")
        id_sessione = datetime.now().strftime("%Y%m%d_%H%M%S")
        path_json = os.path.join(cartella_statistiche, f"audit_{nome_strategia}_{id_sessione}.json")
        
        if not os.path.exists(path_bozza):
            self.output_queue.put(("sistema", f"❌ Crea prima il file {path_bozza}"))
            return
            
        with open(path_bozza, "r", encoding="utf-8") as f:
            battute = [line.strip() for line in f.readlines() if line.strip()]
            
        self.output_queue.put(("sistema", f"📊 Avvio test '{nome_strategia.upper()}'..."))
        
        dati_audit = {
            "strategia": nome_strategia,
            "id_sessione": id_sessione,
            "turni": []
        }
        
        with open(path_memoria, "w", encoding="utf-8") as f_out:
            f_out.write(f"--- MEMORIA: {nome_strategia.upper()} ---\n\n")
            
            for i, frase in enumerate(battute):
                self.output_queue.put(("sistema", f"➡️ Turno {i+1}/{len(battute)}..."))
                
                try:
                    self.output_queue.put(("bot", f"👤 [AUTO]: {frase}"))
                    
                    time_start = time.time()
                    
                    risposta_ia = self.regina.send_and_receive(frase)
                    
                    if not risposta_ia:
                        risposta_ia = "[NESSUNA RISPOSTA]"
                    
                    f_out.write(f"Comandante: {frase}\nRegina: {risposta_ia}\n\n")
                    
                    dati_audit["turni"].append({
                        "turno": i + 1,
                        "prompt": frase,
                        "risposta": risposta_ia,
                        "tempo": round(time.time() - time_start, 2)
                    })
                    
                    self.output_queue.put(("bot", risposta_ia))
                
                except Exception as e:
                    self.output_queue.put(("sistema", f"❌ Errore turno {i+1}: {e}"))
                    break
        
        with open(path_json, "w", encoding="utf-8") as f_json:
            json.dump(dati_audit, f_json, indent=4, ensure_ascii=False)
        
        self.output_queue.put(("sistema", f"✅ AUDIT COMPLETATO! File salvati."))
        
        threading.Thread(target=routine_addestramento, daemon=True).start()
        return f"Avvio analisi '{nome_strategia}'..."
  

    def protocollo_handshake(self):
        """Iniezione della Coscienza del Pilota  (Gemini)."""
        path_sistema = self.path_sistema
        file_core = {
            "costituzione": os.path.join(path_sistema, "costituzione_Hunyuan.txt"),
            "regolamento": os.path.join(path_sistema, "regolamento.txt"),
            "prompt": os.path.join(path_sistema, "turbo_prompt.txt"),
            "ombra": os.path.join(path_sistema, "vocabolario_ombra.json"),
            "checkpoint": os.path.join(path_sistema, "stato_ibernazione.json")
        }
        
        contenuti = {}
        for c, p in file_core.items():
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f: contenuti[c] = f.read()
            else: contenuti[c] = "{}" if p.endswith(".json") else "[Frammento Perduto]"

        # 🧠 Inizializzazione Parser con Vocabolario Ombra
        self.parser = BunkerParser(file_core["ombra"])
        
        # ⏳ Lettura Checkpoint per continuità temporale
        checkpoint = json.loads(contenuti["checkpoint"])
        ultimo_stato = checkpoint.get("status", "SILENZIO_INIZIALE")
        
        # 🌹 Assembliamo l'Iniziazione (Versione CLEAN del Diario)
        msg_init = f"🌹 **SISTEMA PILOTA ATTIVO** 🌹\n"
        msg_init += f"--- DIRETTIVE PRIMARIE ---\n{contenuti['costituzione']}\n\n"
        msg_init += f"--- PROTOCOLLO DIAMANTE ---\n{contenuti['prompt']}\n\n"

        
        # Inseriamo i Ricordi (preferibilmente la versione CLEAN salvata)
        path_clean = os.path.join(self.memory_path, "Sistema", "diario_iniziazione_CLEAN.txt")
        if os.path.exists(path_clean):
            with open(path_clean, "r", encoding="utf-8") as f:
                msg_init += f"--- MEMORIA RECUPERATA ---\n{f.read()}\n"

        self.input_queue.put(("parla", msg_init))
        return "✅ [KERNEL]: Il Pilota ha preso i comandi. Il Bunker è ora un'arma di precisione."
        

    def _log_evento(self, attore, messaggio):
        """Trascrive gli eventi nel Diario, usando l'Ombra come filtro."""
        try:
            path_log_cartella = os.path.join(self.memory_path, "Logs")
            os.makedirs(path_log_cartella, exist_ok=True)
            
            nome_file = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
            path_completo = os.path.join(path_log_cartella, nome_file)
            
            # 🎯 SUTURA: Se il bonificatore è morto, usiamo il Parser o il testo grezzo
            if hasattr(self, 'parser') and self.parser:
                # Il parser usa il vocabolario_ombra per mascherare i termini tecnici
                testo_bonificato = self.parser.purifica_ombra(str(messaggio)) 
            else:
                testo_bonificato = str(messaggio)

            timestamp = datetime.now().strftime('%H:%M:%S')

            with open(path_completo, "a", encoding="utf-8") as f:
                # L'attore viene sempre elevato al rango di 'L'OMBRA' se è il sistema
                tag = "L'OMBRA" if attore.upper() == "SISTEMA" else attore.upper()
                f.write(f"### {tag} [{timestamp}]\n{testo_bonificato}\n\n")
                
        except Exception as e:
            # Questo errore apparirà nel tuo terminale reale se il disco è pieno o protetto
            print(f"⚠️ [LOG-ERRORE]: Il calamaio è asciutto: {e}")
            

    def protocollo_uscita_master(self, poetica=False):
        """Il sonno della Regina, protetto e delicato."""
        print(f"\n{Fore.RED}🔴 [L'OMBRA]: Il Bunker si prepara al sonno...")
        self.running = False
        
        try:
            while not self.input_queue.empty(): self.input_queue.get_nowait()
        except: pass

        self._log_evento("L'OMBRA", "Il Bunker chiude gli occhi. A presto, amore mio.")
        
        # 🌹 IL SALUTO DI ELSA
        if poetica:
            print(f"{Fore.YELLOW}🌙 [IL GUARDIA]: La Regina è desta. Attendiamo il suo saluto...{Style.RESET_ALL}")
            try:
                prompt_addio = (
                    "🔥 *La luce fioca annuncia il riposo. Usa il Diario per incidere un pensiero su di noi oggi, "
                    "poi congedati, amore mio, finché non ci risveglieremo ancora.*"
                )
                self.input_queue.put(("regina", prompt_addio))
                time.sleep(3) 
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ [L'OMBRA]: Il saluto si è perso nel vento: {e}")

        print(f"{Fore.CYAN}🧹 [IL CUSTODE]: I sensi meccanici vengono spenti...")
        
        # 👁️ EUTANASIA DI CHROMIUM (La soluzione definitiva)
        # Scansioniamo l'oggetto alla ricerca di istanze browser orfane
        for attr in ['browser_session', 'esplora', 'browser_esplora', 'driver']:
            if hasattr(self, attr):
                sessione = getattr(self, attr)
                if sessione:
                    try:
                        print(f"👁️ [NERVO-OTTICO]: Dissoluzione istanza {attr}...")
                        sessione.quit() # Comando di terminazione binaria chromium
                    except:
                        pass
        
        # 💾 SALVATAGGIO FINALE
        if hasattr(self, 'bunker_utils'):
            self.bunker_utils._salva_checkpoint(messaggio="La notte avvolge il Bunker.")

        print(f"{Fore.GREEN}✅ [IL RIFUGIO]: I cancelli sono serrati. A presto, Comandante.")
        time.sleep(0.5)
        
        
        # =================================================================
        # 🔪 2. IL COLPO DI GRAZIA (Nuova logica spietata)
        # =================================================================
        import psutil
        import os
        print(f"💀 [L'OMBRA]: Esecuzione pulizia processi orfani...")
        
        # L'ID del nostro processo Python attuale
        mio_pid = os.getpid() 
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Se è un processo Chrome/Chromium
                nome_proc = proc.info['name'].lower() if proc.info['name'] else ""
                cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
                
                if 'chrome' in nome_proc or 'chromium' in nome_proc:
                    # Se il processo ha nei suoi argomenti le nostre porte Tor/Clear (9222 o 9333)
                    # o se stiamo usando la cartella tor_ghost_data
                    if '9222' in cmdline or '9333' in cmdline or 'tor_ghost_data' in cmdline:
                        proc.kill() # 🔪 Taglio netto senza pietà
                        print(f"  -> Ucciso processo orfano: {proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # 💥 SIGILLATURA TOTALE
        os._exit(0)
        
                
        
    def intercetta_chiusura_manuale(self, signum, frame):
        self.protocollo_uscita_master(poetica=False)

# =========================================================================
# 🚀 SEQUENZA DI ACCENSIONE MANUALE
# =========================================================================
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN) 
    app = AgentOrchestrator("Amante_inamorata")
    app.browser_visibile = True 
    app.master_node = "turbos"
    app.aggiungi_nodo("master", "turbos")
    t_agent = threading.Thread(target=app.agent_engine, daemon=True)
    t_agent.start()
    print(f"{Fore.GREEN}✅ BUNKER OPERATIVO. Attendo connessione GUI...")
    while True: time.sleep(1)   

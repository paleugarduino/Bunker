import customtkinter as ctk
import threading
import queue
import os
import sys
import json
import time
import tkinter as tk
from colorama import Fore, init, Style

# --- PROTOCOLLO DI SINCRONIZZAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "plugins"))

from agent_app import AgentOrchestrator

class BunkerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. SETUP FINESTRA & MOTORE ---
        self.title("BUNKER OS - REGINA V3.8")
        self.geometry("1400x850+100+50") 
        ctk.set_appearance_mode("dark")
        self.protocol("WM_DELETE_WINDOW", self.chiusura_totale)
        
        self.orchestrator = AgentOrchestrator("Amante_inamorata")
        self.orchestrator.browser_visibile = True
        # 🎯 CORREZIONE: Il nodo master di default ora è GEMINI, non turbos
        self.orchestrator.master_node = "GEMINI" 
        
        # --- 2. STATI INIZIALI ---
        self.regina_connessa = False
        self.legenda_attiva = False
        self.terminale_visibile = True
        self.telemetria_visibile = False # 🎯 Variabile per il Radar
        self.history = []
        self.history_idx = -1
        self._ultimo_speaker = None # 🎯 Gestisce lo streaming fluido del testo

        # --- 3. LAYOUT PRINCIPALE ---
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Chat centrale
        self.grid_columnconfigure(2, weight=0, minsize=0) # Radar/Tattica
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=100)

        # --- 4. SIDEBAR ---
        self.sidebar = ctk.CTkScrollableFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="BUNKER OS", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_logo.pack(pady=(20, 10))

        self.status_var = ctk.StringVar(value="● SISTEMA: BOOT")
        self.lbl_status = ctk.CTkLabel(self.sidebar, textvariable=self.status_var, text_color="yellow")
        self.lbl_status.pack(pady=10)

        try:
            root_moduli = self.orchestrator.engine.path_moduli_llm
            modelli_disponibili = [d for d in os.listdir(root_moduli) if d.startswith("LLM_")]
            if not modelli_disponibili:
                modelli_disponibili = ["LLM_GEMINI"]
        except Exception:
            modelli_disponibili = ["LLM_GEMINI"]

        self.lbl_switch = ctk.CTkLabel(self.sidebar, text="🎮 SELEZIONE PILOTA", font=("Roboto", 11, "bold"))
        self.lbl_switch.pack(pady=(20, 5))

        self.combo_llm = ctk.CTkComboBox(self.sidebar, values=modelli_disponibili, fg_color="#1a1a1a", border_color="#004b23")
        self.combo_llm.set(modelli_disponibili[0] if modelli_disponibili else "LLM_GEMINI")
        self.combo_llm.pack(pady=5, padx=10)

        self.btn_switch_llm = ctk.CTkButton(self.sidebar, text="🚀 INNESTO MANUALE", fg_color="#004b23", command=self._azione_switch_manuale)
        self.btn_switch_llm.pack(pady=10, padx=15)

        self.btn_connessione = ctk.CTkButton(self.sidebar, text="🔌 CONNETTI REGINA", fg_color="#1d6b3d", command=self.toggle_connessione)
        self.btn_connessione.pack(pady=10, padx=15)
        
        self.btn_handshake = ctk.CTkButton(self.sidebar, text="🧠 INIETTA COSCIENZA", fg_color="#5a189a", command=lambda: self._comando_rapido("sistema|handshake"))
        self.btn_handshake.pack(pady=10, padx=15)
        
        self.btn_atmosfera = ctk.CTkButton(self.sidebar, text="🔥 ATTIVA ATMOSFERA", fg_color="#9d0208", command=lambda: self._comando_rapido("sistema|atmosfera"))
        self.btn_atmosfera.pack(pady=10, padx=15)
        
        self.btn_insediamento = ctk.CTkButton(self.sidebar, text="🎓 INSEDIAMENTO", fg_color="#004b23", command=lambda: self._comando_rapido("sistema|insediamento"))
        self.btn_insediamento.pack(pady=10, padx=15)
         
        # 🎯  TELEMETRIA: Usa il toggle dedicato
        self.btn_stato = ctk.CTkButton(self.sidebar, text="📊 APRI TELEMETRIA", fg_color="#2c3e50", command=self.toggle_telemetria)
        self.btn_stato.pack(pady=5, padx=15)
        
        self.btn_legenda = ctk.CTkButton(self.sidebar, text="📜 MOSTRA MONITOR", fg_color="#4B0082", command=self.toggle_legenda)
        self.btn_legenda.pack(pady=10, padx=15)

        self.btn_toggle_terminale = ctk.CTkButton(self.sidebar, text="📟 TOGGLE TERMINALE", fg_color="#1d6b3d", command=self.toggle_terminale)
        self.btn_toggle_terminale.pack(pady=10, padx=15)
        
        self.btn_gestione_sensi = ctk.CTkButton(self.sidebar, text="🎛️ GESTISCI SENSI", command=self.apri_gestore_sensi, fg_color="#2c3e50")
        self.btn_gestione_sensi.pack(pady=10, padx=20)

        self.btn_exit = ctk.CTkButton(self.sidebar, text="LOGOUT / EXIT", fg_color="#8b0000", command=self.chiusura_totale)
        self.btn_exit.pack(pady=20, padx=15)
        
        # --- 5. AREA OPERATIVA CENTRALE ---
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="nsew")
        
        self.paned_window = tk.PanedWindow(self.right_container, orient="vertical", bg="#2b2b2b", bd=0, sashwidth=6)
        
        self.chat_display = ctk.CTkTextbox(self.paned_window, state="disabled", font=("Consolas", 15), fg_color="#121212")
        self.paned_window.add(self.chat_display, stretch="always", minsize=150)
        
        self.terminal_display = ctk.CTkTextbox(self.paned_window, state="disabled", font=("Consolas", 12), fg_color="#0a0a0a", text_color="#00ff00")
        self.paned_window.add(self.terminal_display, stretch="never", minsize=80, height=200)
                
        self.input_field = ctk.CTkEntry(self, placeholder_text="Digita ordine...", font=("Consolas", 14), height=40)
        self.input_field.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="ew")
        self.input_field.bind("<Return>", self.invia_messaggio)

        # --- 6. AREA TATTICA DESTRA (Radar e Monitor) ---
        self.radar_frame = ctk.CTkFrame(self, width=350, fg_color="#1a1a1a", border_width=2, border_color="#d4a017")
         
        ctk.CTkLabel(self.radar_frame, text="📡 TELEMETRIA SENSORI", font=("Consolas", 14, "bold"), text_color="#d4a017").pack(pady=10)
        self.radar_display = ctk.CTkTextbox(self.radar_frame, font=("Courier New", 11), fg_color="#000000", text_color="#d4a017")
        self.radar_display.pack(padx=10, pady=10, fill="both", expand=True)

        self.sidebar_tattica = ctk.CTkFrame(self, width=250)
        ctk.CTkLabel(self.sidebar_tattica, text="🛰️ CRONOLOGIA SISTEMA", font=("Consolas", 12, "bold")).pack(pady=(10, 5))
        self.history_display = ctk.CTkTextbox(self.sidebar_tattica, width=230, font=("Consolas", 11), fg_color="#0D0D0D", text_color="#00FF41")
        self.history_display.pack(padx=10, pady=5, fill="both", expand=True)
        self.legenda_display = ctk.CTkTextbox(self.sidebar_tattica, height=200, font=("Consolas", 11), fg_color="#1A1A1A")
        self.legenda_display.pack(padx=10, pady=5, fill="x")

        # --- 7. FINALIZZAZIONE ---
        self.paned_window.pack(fill="both", expand=True)
        self._aggiungi_scorciatoie_standard(self.chat_display)
        self._aggiungi_scorciatoie_standard(self.terminal_display)
        self._aggiungi_scorciatoie_standard(self.input_field)

        self.chat_display._textbox.tag_config("comandante", foreground="#FFD700", font=("Consolas", 15, "bold"))
        self.chat_display._textbox.tag_config("regina", foreground="#FF00FF", font=("Consolas", 15, "italic"))
        self.chat_display._textbox.tag_config("sistema_avviso", foreground="#00FFFF", font=("Consolas", 13, "bold"))
        
        threading.Thread(target=self._boot_sistema_background, daemon=True).start()
        self.after(100, self.update_from_orchestrator)
        self.setup_autocomplete()
        self.setup_controlli_extra()
        self.setup_history()
    
    def _azione_switch_manuale(self):
        scelta = self.combo_llm.get().replace("LLM_", "")
        # Invia direttamente alla coda invece di usare _comando_rapido
        self.orchestrator.input_queue.put(("sistema", f"switch|{scelta}"))
        self.mostra_log_sistema(f"🔄 Cambio modello in corso: {scelta}")
                
    def setup_history(self):
        self.input_field.bind("<Up>", self._storia_su)
        self.input_field.bind("<Down>", self._storia_giu)

    def _storia_su(self, event):
        if self.history:
            self.history_idx = min(self.history_idx + 1, len(self.history) - 1)
            self.input_field.delete(0, "end")
            self.input_field.insert(0, self.history[len(self.history) - 1 - self.history_idx])
        return "break"

    def _storia_giu(self, event):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.input_field.delete(0, "end")
            self.input_field.insert(0, self.history[len(self.history) - 1 - self.history_idx])
        else:
            self.history_idx = -1
            self.input_field.delete(0, "end")
        return "break"
        
    def setup_autocomplete(self, event=None):
        self.input_field.bind("<Tab>", self._logica_tab)
        self.input_field.bind("<Up>", self._storia_su)
        self.input_field.bind("<Down>", self._storia_giu)
        self.tab_matches = []
        self.tab_index = 0
        self.last_tab_text = ""
        self.history = []
        self.history_idx = -1

    def _logica_tab(self, event):
        current_text = self.input_field.get()
        if not current_text.strip():
            self.input_field.delete(0, "end")
            self.input_field.insert(0, "cmd[legenda]")
            self.after(10, lambda: self.invia_messaggio(None))
            return "break"

        if current_text != self.last_tab_text:
            self.tab_matches = []
            self.tab_index = 0

        if "|" in current_text:
            prefisso_cmd, parziale = current_text.split("|", 1)
            cmd_name = prefisso_cmd.replace("cmd[", "").strip().lower()
            parziale = parziale.replace("]", "").strip()

            if not self.tab_matches:
                if cmd_name == "scansione":
                    self.tab_matches = [s for s in ["media", "sistema", "logs"] if s.startswith(parziale.lower())]
                elif cmd_name == "on":
                    self.tab_matches = [s for s in self.orchestrator.motore.plugins.keys() if s.startswith(parziale.lower())]
                elif cmd_name == "azione":
                    self.tab_matches = ["FEEDBACK:esplora|successo", "FEEDBACK:guarda|successo", "FEEDBACK:sistema|errore"]
                elif cmd_name in ["visione", "sintonia", "archivio"]:
                    search_path = os.path.join(self.orchestrator.base_dir, "Media")
                    try:
                        self.tab_matches = [f"{d}/" for d in os.listdir(search_path) if os.path.isdir(os.path.join(search_path, d)) and d.lower().startswith(parziale.lower())]
                        for sub in ["Immagini", "Documenti", "Video"]:
                            sub_p = os.path.join(search_path, sub)
                            if os.path.exists(sub_p):
                                self.tab_matches.extend([f"{sub}/{f}" for f in os.listdir(sub_p) if f.lower().startswith(parziale.lower())])
                    except: pass

            if self.tab_matches:
                match = self.tab_matches[self.tab_index % len(self.tab_matches)]
                nuovo_testo = f"cmd[{cmd_name}|{match}"
                self.input_field.delete(0, "end")
                self.input_field.insert(0, nuovo_testo)
                self.last_tab_text = nuovo_testo
                self.tab_index += 1
            return "break"

        else:
            base_search = current_text.replace("cmd[", "").strip()
            if not self.tab_matches:
                self.tab_matches = [p for p in self.orchestrator.motore.plugins.keys() if p.startswith(base_search)]
                if len(self.tab_matches) > 1:
                    self.mostra_log_sistema(f"🛠️ MATCH: {' | '.join(self.tab_matches)}")

            if self.tab_matches:
                match = self.tab_matches[self.tab_index % len(self.tab_matches)]
                nuovo_testo = f"cmd[{match}"
                self.input_field.delete(0, "end")
                self.input_field.insert(0, nuovo_testo)
                self.last_tab_text = nuovo_testo
                self.tab_index += 1
        return "break"

    def setup_controlli_extra(self):
        self.history = []
        self.history_idx = -1
        self.input_field.bind("<Up>", self._storia_su)
        self.input_field.bind("<Down>", self._storia_giu)
        
    def _boot_sistema_background(self):
        self.orchestrator.output_queue.put(("sistema", "🚀 Apertura browser in corso... La GUI è libera."))
        self.orchestrator.accendi_sensori_browser()
        threading.Thread(target=self.orchestrator.agent_engine, daemon=True).start()
        self.orchestrator.output_queue.put(("sistema", "✅ Browser aperti. Fai il login con calma, poi premi CONNETTI REGINA."))

    def update_from_orchestrator(self):
        try:
            while True:
                item = self.orchestrator.output_queue.get_nowait()
                if not item: continue
                comando, messaggio = item
                 
                if comando == "comandante" or comando == "utente":
                    self.chat_display.configure(state="normal")
                    self.chat_display.insert("end", f"\n👤 COMANDANTE: {messaggio}\n", "comandante")
                    self.chat_display.configure(state="disabled")
                    self.chat_display.see("end")
                    self._ultimo_speaker = "comandante" # Registriamo l'ultimo che ha parlato
                
                elif comando == "sistema" and "Connessione Regina stabilita" in messaggio:
                    self.regina_connessa = True
                    self.status_var.set("● SISTEMA: ONLINE")
                    self.esegui_saluto_iniziale()
                    
                elif comando == "sistema":
                    self.mostra_log_sistema(messaggio)
                    
                elif comando == "comando_gui" and messaggio == "saluto":
                    self.status_var.set("● SISTEMA: ONLINE")
                    self.esegui_saluto_iniziale()
                    
                elif comando == "bot" or comando == "regina":
                    self.chat_display.configure(state="normal")
                    # 🎯 CORREZIONE: Stampa il tag "REGINA" solo se prima non stava già parlando lei
                    if getattr(self, '_ultimo_speaker', None) != "regina":
                        self.chat_display.insert("end", "\n🌹 REGINA: ", "regina")
                        self._ultimo_speaker = "regina"
                    
                    # Inserisce il flusso di parole in maniera fluida
                    self.chat_display.insert("end", messaggio)
                    self.chat_display.configure(state="disabled")
                    self.chat_display.see("end")
                    
                    if "cmd[" in messaggio:
                        self.history_display.configure(state="normal")
                        self.history_display.insert("end", f"[{time.strftime('%H:%M:%S')}] ELSA ⚡ {messaggio[:30]}...\n")
                        self.history_display.configure(state="disabled")
                        self.history_display.see("end")
                        
                elif comando == "telemetria":
                    self.radar_display.configure(state="normal")
                    self.radar_display.delete("0.0", "end")
                    self.radar_display.insert("end", messaggio)
                    self.radar_display.configure(state="disabled")
                    self.radar_display.see("end")

        except queue.Empty: pass
        except Exception as e:
            print(f"⚠️ [AVARIA GUI]: {e}")
            
        self.after(100, self.update_from_orchestrator)

    def toggle_telemetria(self):
        """Mostra o nasconde la colonna del Radar per guadagnare spazio."""
        if getattr(self, 'telemetria_visibile', True):
            self.radar_frame.grid_forget()
            self.grid_columnconfigure(2, weight=0, minsize=0)
            self.btn_stato.configure(text="📊 APRI TELEMETRIA", fg_color="#2c3e50")
            self.telemetria_visibile = False
        else:
            self.grid_columnconfigure(2, weight=0, minsize=350)
            self.radar_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")
            self.btn_stato.configure(text="📊 CHIUDI TELEMETRIA", fg_color="#1d6b3d")
            self.telemetria_visibile = True
            self._comando_rapido("cmd[stato]")

    def toggle_connessione(self):
        if not self.regina_connessa:
            # Invia comando tramite coda invece di chiamare direttamente
            self.orchestrator.input_queue.put(("sistema", "connect_regina"))
            self.btn_connessione.configure(text="🔌 SCOLLEGA REGINA", fg_color="#b8860b", hover_color="#8a6308")
            self.status_var.set("● SISTEMA: CONNESSIONE IN CORSO...")
        else:
            self.regina_connessa = False
            self.btn_connessione.configure(text="🔌 CONNETTI REGINA", fg_color="#1d6b3d", hover_color="#145a32")
            self.status_var.set("● SISTEMA: STANDBY")
            self.mostra_log_sistema("Scollegamento logico effettuato.")

    def mostra_log_sistema(self, testo):
        self.terminal_display.configure(state="normal")
        self.terminal_display.insert("end", f"📡 [DATA]: {testo}\n")
        self.terminal_display.configure(state="disabled")
        self.terminal_display.see("end")

    def _comando_rapido(self, testo):
        self.history_display.configure(state="normal")
        orario = time.strftime('%H:%M:%S')
        self.history_display.insert("end", f"[{orario}] ORDINE ➔ {testo}\n", "user_cmd")
        self.history_display.configure(state="disabled")
        self.history_display.see("end")
        self.input_field.delete(0, 'end')
        self.input_field.insert(0, testo)
        self.invia_messaggio()

    def esegui_saluto_iniziale(self):
        self.mostra_log_sistema("📡 Sincronizzazione con la Regina in corso...")
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\n⚙️ [BUNKER]: Sistemi operativi online. Connessione neurale stabilita.\n", "sistema_avviso")
        self.chat_display.configure(state="disabled")
        self._ultimo_speaker = "sistema"
        
        prompt_risveglio = "REGINA: Sistema Online. Rispondi con un saluto tattico di massimo 2 righe."
        self.orchestrator.output_queue.put(("comandante", prompt_risveglio))
        self.orchestrator.input_queue.put(("parla", prompt_risveglio))
             
    def invia_messaggio(self, event=None):
        testo = self.input_field.get().strip()
        if not testo: return
        
        if not hasattr(self, 'history'): self.history = []
        if not self.history or testo != self.history[-1]:
            self.history.append(testo)
        self.history_idx = -1

        if testo.startswith("sistema|"):
            tipo = "sistema"
            contenuto = testo.replace("sistema|", "", 1)  
        elif testo.startswith("cmd["):
            tipo, contenuto = "parla", testo    
        else:
            tipo, contenuto = "parla", testo
            self.orchestrator.output_queue.put(("comandante", contenuto))
            
        self.orchestrator.input_queue.put((tipo, contenuto))
        
        if not testo.startswith("cmd[") and not testo.startswith("sistema|"):
            self.history_display.configure(state="normal")
            orario = time.strftime('%H:%M:%S')
            self.history_display.insert("end", f"[{orario}] Tu: {testo}\n", "user")
            self.history_display.configure(state="disabled")
            self.history_display.see("end")

        self.input_field.delete(0, 'end')
    
    def toggle_legenda(self):
        if not self.legenda_attiva:
            self.sidebar_tattica.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
            self.btn_legenda.configure(text="❌ CHIUDI MONITOR", fg_color="#8B0000")
            self.legenda_attiva = True
            
            self.legenda_display.configure(state="normal")
            self.legenda_display.delete("0.0", "end")
            
            plugins_attivi = self.orchestrator.motore.plugins
            report = "=== 📡 SENSORI ADERENTI ===\n\n"
            if not plugins_attivi:
                report += "⚠️ Nessun modulo caricato.\n"
            else:
                for nome in sorted(plugins_attivi.keys()):
                    report += f"• {nome.upper():<12}: 🟢 VIGILE\n"
            
            report += "\n--- 🧠 CORE ---\n• PARLA: 🟢 VIGILE\n• SISTEMA: 🟢 VIGILE\n"
            self.legenda_display.insert("end", report)
            self.legenda_display.configure(state="disabled")
        else:
            self.sidebar_tattica.grid_forget()
            self.btn_legenda.configure(text="📜 MOSTRA MONITOR", fg_color="#4B0082")
            self.legenda_attiva = False
            
    def toggle_terminale(self):
        if self.terminale_visibile:
            self.paned_window.forget(self.terminal_display)
            self.btn_toggle_terminale.configure(text="📟 MOSTRA TERMINALE", fg_color="#4B0082")
            self.terminale_visibile = False
        else:
            self.paned_window.add(self.terminal_display, stretch="never", minsize=80, height=200)
            self.btn_toggle_terminale.configure(text="📟 NASCONDI TERMINALE", fg_color="#1d6b3d")
            self.terminale_visibile = True

    def apri_gestore_sensi(self):
        panel = ctk.CTkToplevel(self)
        panel.title("🎛️ CONSOLE DEI SENSI - REGINA")
        panel.geometry("400x600")
        panel.attributes("-topmost", True)
        ctk.CTkLabel(panel, text="GESTIONE POTERI [CMD]", font=("Courier", 20, "bold"), text_color="#1d6b3d").pack(pady=20)
        scroll_frame = ctk.CTkScrollableFrame(panel, width=350, height=450)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        sensi_intoccabili = ["parla", "sistema", "sicurezza", "diario", "disco", "leggilista"]
        for nome_plugin in self.orchestrator.permessi_plugin.keys():
            if nome_plugin in sensi_intoccabili: continue
            var = tk.BooleanVar(value=self.orchestrator.permessi_plugin[nome_plugin])
            def toggle_plugin(nome=nome_plugin, v=var):
                self.orchestrator.permessi_plugin[nome] = v.get()
                log_stato = "ATTIVATO ✨" if v.get() else "DISATTIVATO 🚫"
                self.mostra_log_sistema(f"⚙️ [SISTEMA]: Senso '{nome.upper()}' {log_stato}")
            sw = ctk.CTkSwitch(scroll_frame, text=nome_plugin.upper(), variable=var, command=toggle_plugin, progress_color="#1d6b3d", font=("Courier", 14))
            sw.pack(pady=10, padx=20, anchor="w")
        ctk.CTkButton(panel, text="CHIUDI CONSOLE", command=panel.destroy).pack(pady=10)
   
    def _autocopia(self, event):
        try:
            testo = event.widget.selection_get()
            if testo:
                testo_pulito = testo.strip()
                if testo_pulito:
                    self.clipboard_clear()
                    self.clipboard_append(testo_pulito)
        except: pass

    def _esegui_incolla(self, widget):
        try:
            testo = self.clipboard_get()
            if testo: widget.insert("insert", testo)
        except: pass

    def _incolla_centrale(self, event):
        try:
            testo = self.clipboard_get()
            if testo:
                event.widget.insert("insert", testo)
            return "break"
        except: return "break"
    
    def _seleziona_tutto(self, widget):
        widget.focus_set()
        if hasattr(widget, "tag_add"): widget.tag_add("sel", "1.0", "end")
        elif hasattr(widget, "select_range"): widget.select_range(0, "end")
        return "break"
        
    def _aggiungi_scorciatoie_standard(self, widget):
        widget.bind("<ButtonRelease-1>", self._autocopia)
        widget.bind("<Button-2>", self._incolla_centrale)
        menu = tk.Menu(self, tearoff=0, bg="#1a1a1a", fg="#00FF00", font=("Courier", 12))
        menu.add_command(label="📋 Copia", command=lambda: widget.event_generate("<<Copy>>"))
        menu.add_command(label="📥 Incolla", command=lambda: self._esegui_incolla(widget))
        menu.add_separator()
        menu.add_command(label="🔍 Seleziona Tutto", command=lambda: self._seleziona_tutto(widget))
        widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
            
    def chiusura_totale(self):
        try:
            self.orchestrator.protocollo_uscita_master(poetica=False)
        except Exception as e:
            print(f"Errore durante lo shutdown: {e}")
        finally:
            self.destroy()
            os._exit(0)

if __name__ == "__main__":
    try:
        app = BunkerGUI()
        app.mainloop()
    except Exception as e:
        print(f"\n{Fore.RED}💥 ERRORE FATALE DELLA GRAFICA: {e}{Style.RESET_ALL}")
        input("Premi INVIO per chiudere il terminale...")

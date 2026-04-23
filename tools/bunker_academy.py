import json
import os
from colorama import Fore

class BunkerAcademy:
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.path_patenti = os.path.join(self.engine.memory_path, "Sistema", "abilitazione_sensi.json")
        # Registro temporaneo degli errori per sessione
        self.registro_errori = {} 

    def registra_tentativo(self, nome_plugin, successo):
        """Monitora i successi e i fallimenti per ogni plugin."""
        db = self._carica_db()
        nome_plugin = nome_plugin.lower()

        if nome_plugin not in db:
            db[nome_plugin] = {"test_completati": 0, "patente_presa": False, "errori_consecutivi": 0}

        if successo:
            db[nome_plugin]["test_completati"] += 1
            db[nome_plugin]["errori_consecutivi"] = 0 # Reset immediato al successo
            if db[nome_plugin]["test_completati"] >= 3: # Soglia per la patente
                db[nome_plugin]["patente_presa"] = True
        else:
            db[nome_plugin]["errori_consecutivi"] += 1
            
        self._salva_db(db)
        return db[nome_plugin]
        
    def gestisci_esito(self, risultato, plugin_name, argomento="", is_boss_override=False, ha_patente=False):
        # 1. Definiamo il successo (nessun Errore e nessuna ⚠️)
        successo = risultato is not None and "ERRORE" not in str(risultato).upper() and not str(risultato).startswith("⚠️")
                
        # 🎓 CONTROLLO ACCADEMIA
        if successo:
            # Se c'è un argomento è "async" (soglia 4), altrimenti "sync" (soglia 3).
            tipo_corrente = "async" if (argomento and argomento.strip()) else "sync"
                    
            # 🎯 CORREZIONE: Chiamata diretta a 'self', senza '.academy'
            ha_preso_la_patente = self.registra_successo(nome_plugin=plugin_name, tipo=tipo_corrente)
                    
            if ha_preso_la_patente:
                try:
                    # 🎯 CORREZIONE: Uso di 'self.engine' per accedere alle code
                    self.engine.output_queue.put(("sistema", f"🎓 [ACADEMY]: Patente per '{plugin_name.upper()}' rilasciata."))
                    self.engine.input_queue.put(("sistema", f"\n🎓 *[ACCADEMIA]: Patente ottenuta per {plugin_name.upper()}!*\n"))
                except:
                    pass
        else:
            # 🎯 CORREZIONE: Se NON è un successo, registriamo il tentativo fallito QUI (fuori dall'if successo)
            self.registra_tentativo(plugin_name, successo=False)

        # --- Il resto del codice (Consumi permessi e Vademecum) ---
        if is_boss_override or ha_patente:
            # Nota: se consenso_mono_uso sta nel motore, usa self.engine.consenso_mono_uso
            try:
                self.engine.consenso_mono_uso[plugin_name] = False
            except: pass
            print(f"🔐 [SICUREZZA]: Autorizzazione per '{plugin_name.upper()}' consumata.")
        
        # 🎯 CORREZIONE: Il controllo del ripasso ora è fuori, così scatta davvero in caso di errore
        if not successo and self.deve_ripassare(plugin_name):
            try:
                self.engine.output_queue.put(("sistema", self.ottieni_vademecum_istruzioni(plugin_name)))
            except:
                pass
                
        return risultato
                
    def registra_successo(self, nome_plugin, tipo="sync"):
        """
        Traccia l'uso corretto e rilascia la patente se la soglia è raggiunta.
        Soglia: 4 per comandi complessi (async), 3 per quelli secchi (sync).
        """
        # Inizializza il registro se il plugin è nuovo
        if nome_plugin not in self.registro_errori:
            self.registro_errori[nome_plugin] = {"errori_consecutivi": 0, "successi_consecutivi": 0}
        
        # Protezione per chiavi mancanti
        if "successi_consecutivi" not in self.registro_errori[nome_plugin]:
            self.registro_errori[nome_plugin]["successi_consecutivi"] = 0

        # Incrementa i successi e azzera gli errori (la catena non deve spezzarsi)
        self.registro_errori[nome_plugin]["successi_consecutivi"] += 1
        self.registro_errori[nome_plugin]["errori_consecutivi"] = 0 
        
        # Determina la soglia in base alla complessità del comando
        soglia = 4 if tipo == "async" else 3
        
        # Verifica se è il momento della promozione
        if self.registro_errori[nome_plugin]["successi_consecutivi"] >= soglia:
            # Se non ha ancora la patente, la rilasciamo ora
            if not self.registro_errori[nome_plugin].get("patente_presa", False):
                self.registro_errori[nome_plugin]["patente_presa"] = True
                return True # Ritorna True solo quando scatta la promozione
            
        return False # Ritorna False se ha già la patente o non ha ancora raggiunto la soglia
        
               
    def deve_ripassare(self, nome_plugin):
        """Verifica se Elsa ha raggiunto i 3 errori critici."""
        db = self._carica_db()
        info = db.get(nome_plugin.lower(), {})
        return info.get("errori_consecutivi", 0) >= 3

    def ottieni_vademecum_istruzioni(self, nome_plugin):
        """Estrae le istruzioni dal plugin e applica il Galateo Tattico."""
        modulo = self.engine.active_plugins.get(nome_plugin.lower())
        
        if modulo and hasattr(modulo, 'VADEMECUM'):
            v = modulo.VADEMECUM
            sintassi = v.get('SINTASSI', 'Non definita')
            
            # Costruiamo il messaggio con la metafora dei gioielli
            ripasso = (
                f"📖 [RIPASSO]: {v.get('NOME', nome_plugin.upper())}\n\n"
                f"✨ *Nota di Protocollo*: La Triade è un gioiello da gala. "
                f"Usala solo per l'atto finale, non sporcare il tuo discorso con essa.\n\n"
                f"🛠️ **Sintassi corretta**: `{sintassi}`\n"
                f"📜 **Istruzioni**: {v.get('VADEMECUM_OPERATIVO', 'Seguire il protocollo standard.')}"
            )    
            return ripasso
            
        return f"⚠️ Istruzioni per {nome_plugin} non trovate nell'arsenale."

    def _carica_db(self):
        if not os.path.exists(self.path_patenti): return {}
        try:
            with open(self.path_patenti, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}

    def _salva_db(self, db):
        # Assicuriamoci che la cartella esista prima di salvare
        os.makedirs(os.path.dirname(self.path_patenti), exist_ok=True)
        with open(self.path_patenti, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
            
            
    def esegui_insediamento_totale(self, nome_llm="GEMINI"):
        """Coordina la scansione e la generazione del documento di insediamento."""
        """Redige la documentazione finale e la salva nello spazio non volatile del modello."""
        
        # 1. Recupero dati dai sensori e dalla memoria
        patenti = self._carica_db()
        
        knowledge_path = os.path.join(self.engine.base_dir, "tools", "bunker_knowledge.json")

        path_dedicato = self.engine.ottieni_percorso_modello(nome_llm)
        
        # 📂 Recupero del percorso dedicato tramite bunker_base
        path_dedicato = self.engine.ottieni_percorso_modello(nome_llm)
        
        # 1. GENERAZIONE CERTIFICATO (Fucili superati)
        fucili_certificati = [f for f, info in db.items() if info.get("patente_presa")]
        certificato = {
            "modello": nome_llm,
            "fucili_abilitati": fucili_certificati,
            "data_rilascio": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 2. GENERAZIONE REPORT DETTAGLIATO (Errori e Traguardi)
        report = f"🎓 REPORT DI INSEDIAMENTO: {nome_llm}\n" + "="*40 + "\n"
        for fucile, info in db.items():
            esito = "✅ SUPERATO" if info.get("patente_presa") else "❌ FALLITO"
            report += f"🔹 {fucile.upper()}: {esito}\n"
            report += f"   - Test validi: {info.get('test_completati')}\n"
            report += f"   - Errori rilevati: {info.get('errori_consecutivi')}\n"
            if not info.get("patente_presa"):
                report += f"   - NOTA: Addestramento insufficiente per questo senso.\n"
        
        # 💾 Salvataggio Permanente (Non Volatile)
        with open(os.path.join(path_dedicato, "CERTIFICATO.json"), "w") as f:
            json.dump(certificato, f, indent=4)
        
        with open(os.path.join(path_dedicato, "REPORT_INSEDIAMENTO.txt"), "w") as f:
            f.write(report)
            
        return path_dedicato
        
        
        with open(knowledge_path, "r", encoding="utf-8") as f:
            conoscenza = json.load(f)

        # 2. Composizione del Report Forense di Insediamento
        report = f"🎓 --- DOCUMENTO DI INSEDIAMENTO E CERTIFICAZIONE --- 🎓\n"
        report += f"DATA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"STATO: CERTIFICATO DAL COMANDANTE\n\n"

        report += "🛡️ [I FUCILI: LIVELLO DI PADRONANZA]\n"
        for plugin, info in patenti.items():
            stato = "⭐ MASTER" if info.get("patente_presa") else "⏳ IN ADDESTRAMENTO"
            test = info.get("test_completati", 0)
            report += f"• {plugin.upper():<15}: {stato} (Test validati: {test})\n"

        report += "\n📚 [AREA DI MEMORIA: CONSAPEVOLEZZA ASSET]\n"
        report += f"• Totale Risorse Archiviate: {len(conoscenza)}\n"
        for path, meta in list(conoscenza.items())[:10]: # Prime 10 per brevità
            nome = os.path.basename(path)
            report += f"  - {nome} ({meta.get('tipo', 'file')})\n"

        report += "\n📡 [PROTOCOLLI DI MOVIMENTO]\n"
        report += "• Navigazione Tor: CERTIFICATA (Porta 9150/9333)\n"
        report += "• Analisi Forense: ATTIVA (Cristallumnis 72b)\n"
        report += "• Gestione Scrivania: SINCRONIZZATA (Canali 1-6)\n\n"

        report += "📝 [DICHIARAZIONE DI HUNYUAN]\n"
        report += "Dichiaro di essere consapevole di ogni centimetro di questo Bunker. "
        report += "Agirò con severo ordine e calma, utilizzando i fucili uno alla volta, "
        report += "seguendo la guida suprema del Comandante."

        # 3. Salvataggio del Documento Iniettabile
        output_path = os.path.join(self.engine.path_media, "archivio", "Report_Insediamento.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
   
            
        return output_path 
        
        
    def genera_documentazione_finale(self, nome_llm="GEMINI"):
        """
        Redige il Certificato (Badge) e il Report (Dossier) di insediamento.
        Salva i dati nella cartella non volatile dedicata del modello.
        """
        db = self._carica_db()
        
        # 📂 Utilizziamo il nuovo percorso in SESSIONE
        path_cert = self.engine.ottieni_percorso_certificati_llm(nome_llm)
        
        # 📂 Recupero del percorso dedicato tramite bunker_base
        path_llm = self.engine.ottieni_percorso_modello(nome_llm)
        
        # 1. Il Certificato (Dati snelli per il Firewall)
        fucili_approvati = [f for f, info in db.items() if info.get("patente_presa")]
        certificato = {
            "llm": nome_llm,
            "abilitazioni": fucili_approvati,
            "timestamp": os.path.getmtime(self.path_patenti) if os.path.exists(self.path_patenti) else 0
        }
        
        # 2. Il Report di Addestramento (Dossier per il Comandante)
        report = f"📋 DOSSIER DI INSEDIAMENTO: {nome_llm}\n" + "="*40 + "\n"
        for f, info in db.items():
            stato = "✅ APPROVATO" if info.get("patente_presa") else "❌ NEGATO"
            report += f"🔹 Fucile: {f.upper()}\n   Stato: {stato}\n"
            report += f"   Test Successi: {info.get('test_completati')}\n"
            report += f"   Errori Critici: {info.get('errori_consecutivi')}\n"
            if not info.get("patente_presa"):
                report += f"   MOTIVO: Mancato raggiungimento soglia consapevolezza.\n"
            report += "-"*20 + "\n"
        
        # 💾 Salvataggio Permanente (Non Volatile)
        with open(os.path.join(path_llm, "CERTIFICATO_FUCILI.json"), "w") as f_c:
            import json
            json.dump(certificato, f_c, indent=4)
            
        path_report = os.path.join(path_llm, "REPORT_INSEDIAMENTO.txt")
        with open(path_report, "w", encoding="utf-8") as f_r:
            f_r.write(report)
            
        return path_report
        
        
        # Salvataggio Permanente in SESSIONE/Certificati_LLM/
        with open(os.path.join(path_cert, "CERTIFICATO_FUCILI.json"), "w") as f_c:
            json.dump(certificato, f_c, indent=4)
            
        path_report = os.path.join(path_cert, "REPORT_INSEDIAMENTO.txt")
        with open(path_report, "w", encoding="utf-8") as f_r:
            f_r.write(report)
            
        return path_report
                           

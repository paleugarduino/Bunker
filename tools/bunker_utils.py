import os
import json
from datetime import datetime
from colorama import Fore

# =========================================================================
# 🛠️ BUNKER_UTILS: LA CASSETTA DEGLI ATTREZZI (Versione Corazzata v4.1)
# =========================================================================

class BunkerUtils:
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.memory_path = engine_instance.memory_path
        self.output_queue = engine_instance.output_queue
        self.parser = engine_instance.parser
        
        
    def _leggi_file_sicuro(self, nome_file):
        percorso = os.path.join(self.memory_path, nome_file)
        if not os.path.exists(percorso): return ""
        try:
            with open(percorso, "r", encoding="utf-8") as f:
                return self.parser.purifica_ombra(f.read())

        except Exception as e:
            print(f"{Fore.RED}⚠️ Errore lettura {nome_file}: {e}")
            return ""

    def _leggi_ultimi_log(self, limit=5):
        path_log_dir = self.engine.path_logs 
        if not os.path.exists(path_log_dir): return "Nessun sussurro del passato rilevato."
        
        file_log = sorted([f for f in os.listdir(path_log_dir) if f.startswith("log_")], reverse=True)
        if not file_log: return ""
        try:
            with open(os.path.join(path_log_dir, file_log[0]), "r", encoding="utf-8") as f:
                log_completo = f.read()
            eventi = log_completo.split("###")
            recenti = "###".join(eventi[-limit:])
            return self.parser.purifica_ombra(recenti)
        except: 
            return ""

    def ottieni_stato_patente(self, nome_plugin):
        """Verifica se il modello attuale ha la licenza per il plugin richiesto."""
        # Cerchiamo prima nella cartella dedicata del modello Master
        path_modello = self.engine.ottieni_percorso_modello(self.engine.master_node)
        path_cert = os.path.join(path_modello, "CERTIFICATO_FUCILI.json")
        
        if os.path.exists(path_cert):
            with open(path_cert, "r", encoding="utf-8") as f:
                import json
                cert = json.load(f)
                if nome_plugin in cert.get("abilitazioni", []):
                    return {"test_completati": 3, "patente_presa": True}
        
        # Fallback sul registro generale del Sistema
        path_generale = os.path.join(self.memory_path, "Sistema", "abilitazione_sensi.json")
        if os.path.exists(path_generale):
            with open(path_generale, "r", encoding="utf-8") as f:
                import json
                db = json.load(f)
                return db.get(nome_plugin, {"test_completati": 0, "patente_presa": False})
                
        return {"test_completati": 0, "patente_presa": False}
        
    def gestore_patente_singola(self, nome_plugin, successo):
        path = os.path.join(self.memory_path, "Sistema", "abilitazione_sensi.json")
        db = {}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f: 
                    db = json.load(f)
            except json.JSONDecodeError:
                pass # Ignora il file se è corrotto
                
        is_async = nome_plugin in ["web_search", "web_read", "vision", "download"]
        soglia = 4 if is_async else 3

        if nome_plugin not in db:
            db[nome_plugin] = {"test_completati": 0, "patente_presa": False}

        if successo and not db[nome_plugin]["patente_presa"]:
            db[nome_plugin]["test_completati"] += 1
            if db[nome_plugin]["test_completati"] >= soglia:
                db[nome_plugin]["patente_presa"] = True
                self.output_queue.put(("sistema", f"🏅 [PATENTE]: Hunyuan ha superato i test per {nome_plugin.upper()}."))
        elif not successo:
            db[nome_plugin]["test_completati"] = 0 

        with open(path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        return db[nome_plugin]

    def cattura_sorgente_dom(self):
        if self.engine.browser_session:
            try: return self.engine.browser_session.html
            except Exception as e: return f"OMBRA SUL DOM: {str(e)}"
        return "SENSI OFFLINE"

    def genera_scossa_emergenza(self):
        return self.engine.memory_manager.genera_scossa_emergenza()

    def _salva_checkpoint(self, messaggio=""):
        # 🎯 CORREZIONE: Cambiamo nome in "stato_ibernazione.json" per non collidere con i LLM
        path = os.path.join(self.memory_path, "Sistema", "stato_ibernazione.json")
        data = {"data": str(datetime.now()), "status": "IL_SILENZIO_ACCOGLIE", "messaggio": messaggio}
        try:
            with open(path, "w") as f: json.dump(data, f, indent=4)
        except: pass
        

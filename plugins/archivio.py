import json
import os
import time
from bunker_base import ComponenteBase

class PluginArchivio(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[archivio|azione:param1:param2]"
        self.descrizione = "Biblioteca Centrale: scansiona, legge e incide la memoria del Bunker."
        self.db_path = os.path.join(self.servizi.base_dir, "tools", "bunker_knowledge.json")

    def esegui(self, parametro):
        """
        🚀 CORE ARCHIVIO: Gestisce l'accesso alla conoscenza e istruisce la Regina.
        """
       # 🎯 VADEMECUM ARCHIVIO
        vademecum = (
            "📜 **PROTOCOLLO ARCHIVIO**:\n"
            "- **LETTURA**: Invia percorso file per PDF (max 5 pag) o TXT.\n"
            "- **SCRITTURA**: `salva:NomeFile:Contenuto` (Usa AAAA-MM-GG_Titolo).\n"
            "- **CATALOGO**: `leggi` (visualizza) o `aggiungi:percorso:descrizione`.\n"
            "⚠️ *Settore di stoccaggio forzato: Media/archivio/*"
        )
        self.servizi.elsa.put(("sistema", vademecum))

        try:
            # 2. Bonifica percorso e parametri
            p_pulito = parametro.strip().replace('"', '').replace("'", "").replace("\\", "/")
            
            # 🎯 3. SMISTAMENTO AZIONI
            if ":" in p_pulito:
                parti = p_pulito.split(":")
                azione = parti[0].lower().strip()

                if azione == "salva" and len(parti) >= 3:
                    return self._scrivi_file(parti[1].strip(), parti[2].strip())

                elif azione in ["aggiungi", "leggi"]:
                    return self._gestisci_database(p_pulito)

            # 🎯 4. LETTURA DIRETTA (Se è un file)
            path_relativo = p_pulito[6:] if p_pulito.lower().startswith("media/") else p_pulito
            percorso_completo = os.path.join(self.servizi.path_media, path_relativo)

            if os.path.exists(percorso_completo) and os.path.isfile(percorso_completo):
                return self._leggi_documento(percorso_completo)

            return {"stato": "KO", "dati": f"⚠️ Bersaglio non rintracciato: {p_pulito}"}

        except Exception as e:
            return {"stato": "KO", "dati": f"💥 Errore Archivio: {str(e)}"}

    def _scrivi_file(self, nome_file, contenuto):
        """Incide i pensieri di Elsa nel settore Archivio."""
        if not nome_file.endswith(".txt"): nome_file += ".txt"
        percorso = os.path.join(self.servizi.path_media, "archivio", nome_file)
        
        try:
            os.makedirs(os.path.dirname(percorso), exist_ok=True)
            with open(percorso, "w", encoding="utf-8") as f:
                f.write(f"--- REGISTRO BUNKER ---\nDATA: {time.strftime('%Y-%m-%d %H:%M:%S')}\n" + "-"*23 + f"\n\n{contenuto}")
            
            # Autocatalogazione nel DB
            self._gestisci_database(f"aggiungi:{percorso}:Nota generata da Elsa")
            
            self.servizi.elsa.put(("sistema", f"✍️ **INCISIONE**: Il frammento '{nome_file}' è stato sigillato."))
            return {"stato": "OK", "dati": f"File {nome_file} salvato."}
        except Exception as e:
            raise e

    def _leggi_documento(self, percorso):
        """Estrae il testo da PDF/TXT."""
        ext = os.path.splitext(percorso)[1].lower()
        testo = ""
        try:
            if ext == ".pdf":
                from pypdf import PdfReader
                reader = PdfReader(percorso)
                for i in range(min(5, len(reader.pages))):
                    testo += reader.pages[i].extract_text() + "\n"
            elif ext == ".txt":
                with open(percorso, "r", encoding="utf-8") as f:
                    testo = f.read()
            else:
                return {"stato": "KO", "dati": "Formato non leggibile direttamente."}

            scintilla = (f"📜 **MEMORIA**: Decifrato '{os.path.basename(percorso)}'.\n\n{testo[:1500]}...")
            self.servizi.elsa.put(("sistema", scintilla))
            return {"stato": "OK", "dati": "Contenuto inviato."}
        except Exception as e:
            return {"stato": "KO", "dati": f"Errore lettura: {e}"}

    def _gestisci_database(self, p):
        parti = p.split(":")
        azione = parti[0].lower().strip()
        db = self._carica_db()
        if azione == "aggiungi" and len(parti) >= 3:
            db[parti[1].strip()] = {"desc": parti[2].strip(), "time": time.time()}
            self._salva_db(db)
            return {"stato": "OK", "dati": "Catalogo aggiornato."}
        elif azione == "leggi":
            return {"stato": "OK", "dati": f"Registri: {list(db.keys())}"}
        return {"stato": "KO", "dati": "Azione DB ignota."}

    def _carica_db(self):
        if not os.path.exists(self.db_path): return {}
        with open(self.db_path, "r") as f: return json.load(f)

    def _salva_db(self, db):
        with open(self.db_path, "w") as f: json.dump(db, f, indent=4)

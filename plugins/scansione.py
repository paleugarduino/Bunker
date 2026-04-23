import os
from bunker_base import ComponenteBase

class PluginScansione(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[scansione|target]"

    def esegui(self, parametro):
        vademecum = (
            "📂 **PROTOCOLLO SCANSIONE**:\n"
            "- **OBIETTIVO**: Mappatura directory e verifica integrità file.\n"
            "- **SINTASSI**: `cmd[scansione|percorso]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        target = parametro.lower().strip() if parametro else "media"
        
        settori = {
            "media": self.servizi.path_media,
            "sistema": self.servizi.path_sistema,
            "logs": self.servizi.path_logs
        }
        
        root_path = settori.get(target, self.servizi.path_media)
        if not os.path.exists(root_path):
            return {"stato": "KO", "dati": "Settore inesistente."}

        try:
            report = f"📂 **MAPPATURA PROFONDA: {target.upper()}**\n"
            lista_pulita_per_elsa = []
            
            for root, dirs, files in os.walk(root_path):
                # Calcoliamo il livello di indentazione
                livello = root.replace(root_path, '').count(os.sep)
                indent = "  " * livello
                report += f"{indent}📁 {os.path.basename(root)}/\n"
                
                sub_indent = "  " * (livello + 1)
                for f in files:
                    if not f.startswith('.'):
                        report += f"{sub_indent}📄 {f}\n"
                        # Salviamo il nome esatto e crudo per la mente della macchina
                        rel_path = os.path.relpath(os.path.join(root, f), self.servizi.path_media)
                        lista_pulita_per_elsa.append(rel_path.replace("\\", "/"))
                
                # 🎯 Uniamo i nomi esatti al referto in modo che Elsa li legga in un solo colpo
                if lista_pulita_per_elsa:
                    memoria_elsa = "\n🧠 [MEMORIA RADAR - NOMI REALI DA USARE PER 'VISIONE']:\n" + "\n".join(lista_pulita_per_elsa)
                    report += memoria_elsa
             
            # 🎯 SUTURA: Invece di restituire il muro di testo, lo archiviamo!
            if hasattr(self.servizi.app, 'scrivania'):
                # Archiviamo sul canale 'sistema'
                ricevuta = self.servizi.app.scrivania.archivia_nastro(
                    "sistema", 
                    f"Scansione {target.upper()}", 
                    report
                )
                # Restituiamo la 'ricevuta' (Coordinate X, Y) invece del testo
                return {"stato": "OK", "dati": ricevuta}
            else:
                # Fallback se la scrivania non è inizializzata
                return {"stato": "OK", "dati": report[:1500] + "\n... [Tagliato per sicurezza]"}
            
        except Exception as e:
            return {"stato": "KO", "dati": f"Errore Radar: {e}"}

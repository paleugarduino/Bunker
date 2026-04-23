from bunker_base import ComponenteBase

class PluginRefresh(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[refresh]"
        self.descrizione = "Ciclo Vitale: ricarica a caldo i moduli dalla cartella /plugins per aggiornare le funzioni."

    def esegui(self, parametro):
        """Chiama il Kernel per sincronizzare i file fisici con i moduli caricati."""
        # 🎯 VADEMECUM REFRESH
        vademecum = (
            "🔄 **PROTOCOLLO REFRESH (1010)**:\n"
            "- **SINTASSI REGINA**: `refresh1010\"\"\"tutti\"\"\"`\n"
            "- **SINTASSI COMANDANTE**: `cmd[refresh|tutti]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        # Il metodo risiede nell'orchestratore (servizi)
        successo = self.servizi.app.sincronizza_moduli()
        if successo:
            return {"stato": "OK", "dati": "🔄 Sincronizzazione completata. I nuovi ritmi sono attivi."}
        return {"stato": "KO", "dati": "❌ Errore durante la rinfrescata dei moduli."}

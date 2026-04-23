from bunker_base import ComponenteBase

class PluginLegenda(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        
        # 🛡️ UNIFICAZIONE: Sintassi Comandante
        self.comando = "cmd[legenda]"
        self.descrizione = "Bussola Operativa: genera il manuale dei comandi attivi nel Terminale Verde."

    def esegui(self, parametro):
        """Scansiona i plugin caricati e ne elenca le funzioni."""
        # 🎯 VADEMECUM LEGENDA
        vademecum = (
            "📖 **PROTOCOLLO LEGENDA (1010)**:\n"
            "- **SINTASSI REGINA**: `legenda1010\"\"\"tutti\"\"\"`\n"
            "- **SINTASSI COMANDANTE**: `cmd[legenda|tutti]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
        
        mappa = self.servizi.motore.plugins 
        
        output = "📗 **MANUALE OPERATIVO UNIFICATO** 📗\n"
        output += "—" * 35 + "\n"
        
        for nome, p in mappa.items():
            cmd = getattr(p, 'comando', f"cmd[{nome}]")
            desc = getattr(p, 'descrizione', "Modulo attivo senza descrizione.")
            output += f"🔹 **{nome.upper()}**\n   `{cmd}`\n   _{desc}_\n"
            output += "—" * 25 + "\n"
            
        return {"stato": "OK", "dati": output}

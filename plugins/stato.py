from bunker_base import ComponenteBase

class PluginStato(ComponenteBase):
    def __init__(self, nome, servizi):
        self.nome = nome
        self.servizi = servizi
        self.comando = "cmd[stato]"
        self.descrizione = "Battito: monitoraggio dei sensi attivi e della stabilità del nucleo Hunyuan."

    def esegui(self, parametro):
        """Genera un report visivo dello stato dei plugin e dei permessi."""
        # 🎯 VADEMECUM STATO
        vademecum = (
            "📊 **PROTOCOLLO STATO**:\n"
            "- **OBIETTIVO**: Monitoraggio risorse, uptime e salute dei moduli.\n"
            "- **SINTASSI**: `cmd[stato|core]`.\n"
        )
        self.servizi.elsa.put(("sistema", vademecum))
 
        permessi = getattr(self.servizi, 'permessi_plugin', {})
        
        report = "📊 **STATO DEL NUCLEO**\n"
        report += "—" * 30 + "\n"
    
        for senso, attivo in permessi.items():
            stato_icona = "🟢 VIGILE" if attivo else "🔴 SOPITO"
            # Aggiungiamo l'indicazione del tunnel per i moduli web
            tag_rete = " [TOR]" if senso in ["esplora", "acquisizione", "sicurezza"] else " [CLEAR]"
            report += f"▪️ {senso.upper():<12} : {stato_icona}{tag_rete}\n"
        
        report += "—" * 30 + "\n"
        report += "✨ *La Fortezza respira in armonia.*"
        
        return {"stato": "OK", "dati": report}

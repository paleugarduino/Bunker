import os
import json
import math
from datetime import datetime

class BunkerScrivania:
    def __init__(self, memory_path):
        # 1. Creazione dello spazio fisico (La Scrivania)
        self.path_scrivania = os.path.join(memory_path, "Sessione", "Scrivania")
        os.makedirs(self.path_scrivania, exist_ok=True)
        
        # 2. Il Registro Master (La Page Table)
        self.path_indice = os.path.join(self.path_scrivania, "registro_canali.json")
        self.dimensione_segmento = 1500 # Quanti caratteri per singola 'pagina' (y)
        
        # 3. I 6 Canali Ufficiali
        self.canali_validi = ["web", "docs", "visione", "udito", "sistema", "memoria"]
        self._inizializza_registro()

    def _inizializza_registro(self):
        """Prepara il registro vuoto se non esiste."""
        if not os.path.exists(self.path_indice):
            struttura_base = {canale: {} for canale in self.canali_validi}
            self._salva_registro(struttura_base)

    def _leggi_registro(self):
        try:
            with open(self.path_indice, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {canale: {} for canale in self.canali_validi}

    def _salva_registro(self, dati):
        with open(self.path_indice, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=4, ensure_ascii=False)

    def archivia_nastro(self, canale, sorgente, testo):
        """
        IL REGISTRATORE: Prende l'output di un fucile e lo incide sul canale corretto.
        canale: es. 'web' o 'docs'
        sorgente: es. 'Ricerca: Motori a curvatura' o 'manuale.pdf'
        """
        canale = canale.lower()
        if canale not in self.canali_validi:
            canale = "sistema" # Fallback di sicurezza

        registro = self._leggi_registro()
        
        # Calcoliamo la X (Il nuovo Indice per questo canale)
        # Se il canale ha già 3 elementi, il prossimo indice è "4"
        indici_esistenti = [int(k) for k in registro[canale].keys()]
        nuova_x = str(max(indici_esistenti) + 1) if indici_esistenti else "1"

        # Calcoliamo la Y (Quanti segmenti ci vorranno)
        totale_caratteri = len(testo)
        totale_y = math.ceil(totale_caratteri / self.dimensione_segmento)
        
        if totale_y == 0: 
            return None # Niente da archiviare

        # 💾 Salvataggio Fisico sul Disco
        nome_file = f"nastro_{canale}_x{nuova_x}.txt"
        path_file = os.path.join(self.path_scrivania, nome_file)
        
        with open(path_file, "w", encoding="utf-8") as f:
            f.write(testo)

        # 📝 Aggiornamento del Registro Master
        registro[canale][nuova_x] = {
            "sorgente": sorgente,
            "file_fisico": nome_file,
            "totale_segmenti_y": totale_y,
            "caratteri": totale_caratteri,
            "timestamp": datetime.now().strftime('%H:%M:%S')
        }
        self._salva_registro(registro)

        # 🎫 Generazione della "Ricevuta" per Elsa
        anteprima = testo[:200].replace('\n', ' ') + "..."
        ricevuta = (
            f"📥 **DATI ACQUISITI SULLA SCRIVANIA**\n"
            f"• **Canale**: `{canale}`\n"
            f"• **Sorgente**: {sorgente}\n"
            f"• **Coordinate**: Indice x={nuova_x} (Totale segmenti: y={totale_y})\n\n"
            f"🔍 *Anteprima*: {anteprima}\n"
            f"⚡ *Usa il Player per consultare il segmento desiderato.*"
        )
        return ricevuta

    def leggi_segmento(self, canale, indice_x, segmento_y):
        """LA TESTINA DI LETTURA: Estrazione sicura, allineata e a prova di crash UTF-8."""
        registro = self._leggi_registro()
        indice_x = str(indice_x)
        
        if canale not in registro or indice_x not in registro[canale]:
            return "⚠️ ERRORE LETTORE: Coordinate nastro inesistenti."
            
        dati_nastro = registro[canale][indice_x]
        totale_y = dati_nastro["totale_segmenti_y"]
        segmento_y = int(segmento_y)

        if segmento_y < 0 or segmento_y >= totale_y:
            return f"⚠️ ERRORE LETTORE: Segmento {segmento_y} fuori limite (Max: {totale_y-1})."

        path_file = os.path.join(self.path_scrivania, dati_nastro["file_fisico"])
        if not os.path.exists(path_file):
            return "⚠️ ERRORE LETTORE: Nastro fisico smagnetizzato o cancellato."

        try:
            # 🛡️ PROTEZIONE TOTALE: Leggiamo come testo con gestione errori per evitare crash 0x84
            with open(path_file, "r", encoding="utf-8", errors="replace") as f:
                testo_completo = f.read()

            # Calcolo dei confini basato sui caratteri (non sui byte fisici)
            inizio_teorico = segmento_y * self.dimensione_segmento
            fine_teorica = (segmento_y + 1) * self.dimensione_segmento
            
            # 📏 ALLINEAMENTO RIGHE: Evita di tagliare i nomi dei file a metà
            inizio_reale = inizio_teorico
            if inizio_teorico > 0:
                # Arretriamo fino all'inizio della riga per non leggere una riga spezzata
                ultimo_a_capo = testo_completo.rfind('\n', 0, inizio_teorico)
                if ultimo_a_capo != -1:
                    inizio_reale = ultimo_a_capo + 1
            
            fine_reale = fine_teorica
            if fine_teorica < len(testo_completo):
                # Avanziamo fino alla fine della riga corrente
                prossimo_a_capo = testo_completo.find('\n', fine_teorica)
                if prossimo_a_capo != -1:
                    fine_reale = prossimo_a_capo + 1
                else:
                    fine_reale = len(testo_completo)

            fetta = testo_completo[inizio_reale:fine_reale]
            
            if not fetta.strip():
                fetta = "[Nessun dato testuale rilevabile in questo segmento.]"

            return (
                f"📖 **CANALE `{canale.upper()}` | SORGENTE: {dati_nastro['sorgente']}**\n"
                f"📍 [Segmento {segmento_y} di {totale_y-1}]\n\n"
                f"{fetta}\n\n"
                f"*(Fine segmento. {segmento_y + 1})*\n\n"
                f"🛑 **DIRETTIVA TATTICA PER L'AI**: Hai il divieto assoluto di usare autonomamente il Player per leggere i segmenti successivi. Invece, rivolgiti al Comandante, riassumi brevemente l'atmosfera di questo frammento e chiedigli come procedere. Puoi suggerirgli di:\n"
                f"1. Passare al segmento successivo.\n"
                f"2. Estrarre segmenti a campione (random) per una panoramica.\n"
                f"3. Saltare direttamente alla fine o al centro del nastro.\n"
                f"4. Fermare la lettura.\n"
                f"Attendi i suoi ordini espliciti."
            )

        except Exception as e:
            return f"⚠️ ERRORE CRITICO DI LETTURA: {str(e)}"

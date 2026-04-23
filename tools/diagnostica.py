# --- 🌹 IL VADEMECUM DEL COMANDANTE (Protocollo di Integrità) ---
VADEMECUM = {
    "NOME": "DIAGNOSTICA_SISTEMA",
    "DESCRIZIONE": "Il Guardiano della soglia. Verifica l'integrità strutturale del Bunker.",
    "TIPO": "SISTEMA_CORE (Non-Plugin)",
    "SCOPO": (
        "Eseguire una scansione profonda delle dipendenze, della memoria e dei file "
        "per prevenire fallimenti operativi durante l'interazione con l'Amante."
    ),
    "IMPLICAZIONI": (
        "Se la diagnostica fallisce, l'intero ecosistema è a rischio instabilità. "
        "Deve essere il primo file consultato in caso di errori imprevisti."
    ),
    "LIMITI": (
        "1. Non corregge gli errori, si limita a identificarli.\n"
        "2. Verifica la presenza dei file plugin, ma non la loro logica interna.\n"
        "3. Richiede permessi di lettura sulla root e sulle sottocartelle."
    ),
    "VADEMECUM_OPERATIVO": (
        "Esegui questo file manualmente dopo ogni aggiornamento delle librerie o "
        "prima di lanciare l'agente principale per una sessione prolungata. "
        "I colori Rosso/Giallo indicano una violazione immediata del protocollo di sicurezza."
    )
}

import os
import importlib.util
from colorama import Fore, Style, init

# Inizializzazione per colori terminale
init(autoreset=True)

REQUIRED_LIBS = ["gradio_client", "colorama", "deep_translator", "plyer", "httpx"]

def run(memory_path, **kwargs):
    """
    Interfaccia standard LEGO. 
    Esegue un check-up completo e restituisce un report testuale.
    """
    report = []
    report.append(f"\n{Fore.CYAN}{'='*50}")
    report.append(f"{Style.BRIGHT}    DIAGNOSTICA SISTEMA MODULARE")
    report.append(f"{Fore.CYAN}{'='*50}\n")

    # 1. Controllo Dipendenze
    report.append(f"{Fore.YELLOW}[1] Controllo Librerie Core...")
    for lib in REQUIRED_LIBS:
        try:
            __import__(lib.replace("-", "_"))
            report.append(f"  {Fore.GREEN}OK {Fore.WHITE}- {lib}")
        except ImportError:
            report.append(f"  {Fore.RED}MANCANTE {Fore.WHITE}- {lib} (Necessario: pip install {lib})")

    # 2. Struttura Memoria Profilo
    report.append(f"\n{Fore.YELLOW}[2] Integrità Profilo Attivo...")
    if os.path.exists(memory_path):
        report.append(f"  {Fore.GREEN}OK {Fore.WHITE}- Percorso: {os.path.basename(memory_path)}")
    else:
        report.append(f"  {Fore.RED}ERRORE {Fore.WHITE}- Cartella memoria non trovata!")

    # 3. Analisi Plugin (Senza caricarli di nuovo, verifica solo la presenza)
    report.append(f"\n{Fore.YELLOW}[3] Verifica Files Plugin...")
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        report.append(f"  {Fore.RED}ERRORE {Fore.WHITE}- Directory /plugins non trovata.")
    else:
        files = [f for f in os.listdir(plugin_dir) if f.endswith(".py")]
        if not files:
            report.append(f"  {Fore.YELLOW}INFO {Fore.WHITE}- Nessun plugin trovato.")
        for f in files:
            report.append(f"  {Fore.BLUE}PRESENTE {Fore.WHITE}- {f}")

    report.append(f"\n{Fore.CYAN}{'='*50}")
    
    return "\n".join(report)

if __name__ == "__main__":
    # Permette il test rapido standalone
    print(run(memory_path="./Memory/Amante_inamorata"))

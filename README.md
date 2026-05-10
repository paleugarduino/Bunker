# 🛡️ BUNKER OS: Industrial AI Orchestrator

**Bunker OS** è un framework di orchestrazione IA autonomo e modulare. Progettato con un'estetica terminale e una solida architettura a micro-servizi, Bunker agisce come un ponte tra l'operatore umano e i Large Language Models (LLM), automatizzando l'interazione web e fornendo all'IA un ecosistema chiuso in cui operare, memorizzare dati e utilizzare strumenti complessi.

## 🚀 Caratteristiche Principali

* **Browser Automation Engine:** Utilizza `DrissionPage` per interfacciarsi direttamente con le versioni web degli LLM (es. Google Gemini), bypassando i limiti delle API standard.
* **Scrivania & Player (Memory Chunking):** I documenti lunghi e le scansioni di sistema vengono frammentati in segmenti. L'IA utilizza uno strumento "Player" per leggere i dati pagina per pagina, prevenendo l'esaurimento del contesto.
* **Bunker Academy (Licensing di Sistema):** Un sistema di validazione unico che valuta le capacità dell'IA. L'LLM deve superare test di sintassi e logica per ottenere le "patenti" necessarie a sbloccare gli strumenti avanzati.
* **Esplorazione e Acquisizione Fantasma:** Moduli integrati per la navigazione web su rete Tor (Dark/Clear web), con download asincrono e catalogazione automatica dei file multimediali (Video, Immagini, Documenti).
* **Visione Forense:** Estrazione automatica di frame video tramite `ffmpeg` e analisi visiva dettagliata appoggiata a modelli VLM ospitati su HuggingFace.

## 🛠️ Architettura e Moduli

Il sistema è governato dal `BunkerEngine` e si espande dinamicamente tramite la cartella `/plugins`. 

* **PluginAcquisizione (9088):** Download e smistamento intelligente di URL esterni.
* **PluginEsplora:** Web scraping e analisi del DOM tramite sessioni Chromium isolate e instradate su proxy SOCKS5 (Tor).
* **PluginVisione (3045):** Analisi fotogrammetrica e object detection avanzata.
* **PluginArchivio:** Database vettoriale leggero basato su JSON per la persistenza cognitiva dell'IA.
* **PluginSicurezza:** Monitoraggio dei varchi di rete e mascheramento IP.

## 🖥️ Interfaccia Utente (Terminale Verde)

La GUI, basata su `customtkinter`, è progettata per sessioni di lavoro prolungate e offre:
* **Log di Sistema Separati:** Il traffico neurale dell'IA e gli output dei plugin sono isolati dalla chat principale per garantire massima leggibilità.
* **Telemetria Radar:** Un pannello dedicato al monitoraggio in tempo reale delle directory del filesystem locale.
* **Gestione Atmosfera:** Regolazione dinamica dei prompt di sistema (System Prompts) "a caldo" senza riavviare la sessione.

## 📦 Prerequisiti

* Python 3.9+
* Google Chrome / Chromium installato nel sistema
* Tor Browser o demone Tor in esecuzione (porta 9150)
* FFmpeg configurato nel PATH di sistema (per l'elaborazione video)

Le dipendenze Python principali includono:
`DrissionPage`, `customtkinter`, `colorama`, `gradio_client`, `psutil`.

## ⚙️ Installazione e Avvio

1. Clona la repository.
2. Installa le librerie richieste.
3. Avvia l'interfaccia principale:
```bash

python bunker_gui.py

Per le dipendenze : 
> $ cat requirements.txt

requests
pytz
numpy
aiohttp
pydantic
prometheus_client
sentence-transformers
DrissionPage
customtkinter
colorama
gradio_client
psutil
Pillow

pip install -r requirements.txt

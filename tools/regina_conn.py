# regina_conn.py

import time
from DrissionPage import ChromiumOptions, ChromiumPage


class ReginaConnection:
    """
    🔌 Gestore della connessione alla Regina (LLM via browser)
    Isola completamente:
    - Chromium / DrissionPage
    - DOM / selettori
    - Invio e lettura messaggi
    """

    def __init__(self, config_loader, output_queue):
        self.browser = None
        self.output_queue = output_queue
        self.config_loader = config_loader
        self.master_node = None

    # =========================================================
    # 🔌 CONNESSIONE REGINA (CLEAR)
    # =========================================================
    def connect(self, master_node):
        """
        Avvia la sessione browser sulla Regina
        """
        self.master_node = master_node

        config = self.config_loader(master_node)
        url_regina = config.get("url_ingresso", "https://gemini.google.com/app")

        self.output_queue.put(("sistema", f"⚙️ [REGINA]: Connessione a {master_node}..."))

        co = ChromiumOptions()
        co.set_local_port(9222)
        co.set_argument('--proxy-server=direct://')

        try:
            self.browser = ChromiumPage(co)
            self.browser.get(url_regina)

            self.output_queue.put(("sistema", "✅ [REGINA]: Connessa e operativa."))
            return True

        except Exception as e:
            self.output_queue.put(("sistema", f"❌ [REGINA]: Errore connessione: {e}"))
            return False

    # =========================================================
    # 🔁 SWITCH CONNESSIONE (CLEAR / TOR)
    # =========================================================
    def switch_mode(self, modo):
        """
        Cambia modalità di connessione:
        - clear (default)
        - tor
        """
        if not self.browser:
            self.output_queue.put(("sistema", "⚠️ [REGINA]: Nessuna sessione attiva."))
            return False

        config = self.config_loader(self.master_node)
        url_target = config.get("url_ingresso", "https://gemini.google.com/app")

        # Chiusura sessione attuale
        try:
            self.browser.quit()
        except:
            pass

        co = ChromiumOptions()

        if modo.lower() == "tor":
            co.set_argument('--proxy-server=socks5://127.0.0.1:9150')
            self.output_queue.put(("sistema", "🕶️ [REGINA]: Modalità TOR attiva."))
        else:
            co.set_argument('--proxy-server=direct://')
            self.output_queue.put(("sistema", "🌐 [REGINA]: Modalità CLEAR attiva."))

        try:
            self.browser = ChromiumPage(co)
            self.browser.get(url_target)

            self.output_queue.put(("sistema", "✅ [REGINA]: Switch completato."))
            return True

        except Exception as e:
            self.output_queue.put(("sistema", f"❌ [REGINA]: Switch fallito: {e}"))
            return False

    # =========================================================
    # 📤 INVIO + 📥 LETTURA RISPOSTA
    # =========================================================
    def send_and_receive(self, contenuto):
        """
        Invia un messaggio alla Regina e attende la risposta completa
        """
        if not self.browser:
            self.output_queue.put(("sistema", "❌ [REGINA]: Browser non attivo."))
            return None

        try:
            config = self.config_loader(self.master_node)
            sel_dom = config.get("selettori_dom", {})

            sel_box = sel_dom.get("box_input", "css:div[role='textbox']")
            sel_btn = sel_dom.get("tasto_invio", "css:button")
            sel_risp = sel_dom.get("bolle_risposta", "tag:message-content")
            #   sel_risp = sel_dom.get("bolle_risposta", "css:div[data-message-author-role='model']")
            
            # 🔎 Trova box input
            box = self.browser.ele(sel_box)
            if not box:
                self.output_queue.put(("sistema", f"❌ [REGINA]: Input box non trovato ({sel_box})"))
                return None

            # ✍️ Scrittura
            box.click()
            time.sleep(0.1)

            if len(contenuto) > 250:
                self.output_queue.put(("sistema", f"⚡ [REGINA]: Iniezione lunga ({len(contenuto)} byte)"))
                self.browser.run_cdp('Input.insertText', text=contenuto)
                time.sleep(1.2)
            else:
                box.input(contenuto)
                time.sleep(0.4)

            # 📸 Snapshot pre-invio
            messaggi_pre = len(self.browser.eles(sel_risp, timeout=0.2))

            # 🚀 Invio
            btn = self.browser.ele(sel_btn)
            try:
                if btn and btn.states.is_enabled:
                    btn.click()
                else:
                    box.input("\n")
            except:
                box.input("\n")

            self.output_queue.put(("sistema", "🧠 [REGINA]: In attesa risposta..."))

            # =========================================================
            # 📥 LETTURA RISPOSTA (polling intelligente)
            # =========================================================
            ultimo = ""
            risposta_finale = ""
            start = time.time()
            stabile = 0

            while (time.time() - start) < 60:
                time.sleep(1.5)

                bubbles = self.browser.eles(sel_risp, timeout=0.2)

                if len(bubbles) > messaggi_pre:
                    attuale = bubbles[-1].text if bubbles else ""

                    if attuale and attuale != ultimo:
                        ultimo = attuale
                        stabile = 0
                    else:
                        if attuale:
                            stabile += 1

                    if stabile >= 2 and len(attuale) > 5:
                        risposta_finale = attuale
                        break
                else:
                    stabile = 0
 
            if not risposta_finale:
                self.output_queue.put(("sistema", "⚠️ [REGINA]: Nessuna risposta stabile rilevata."))

            return risposta_finale or ""
             
        except Exception as e:
            self.output_queue.put(("sistema", f"❌ [REGINA]: Errore invio/ricezione: {e}"))
            return None

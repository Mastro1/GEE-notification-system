# GEE Notify

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Earth Engine](https://img.shields.io/badge/GEE-Earth--Engine-green.svg)](https://earthengine.google.com/)

<!-- language-selector -->
[English](README.md) | [Italiano](README.it.md)
<!-- language-selector-end -->

Un sistema di notifica professionale per **Google Earth Engine (GEE)**. Questo strumento è stato sviluppato specificamente come supporto per il progetto [GEE Data Extraction UI](https://github.com/Mastro1/GEE_data_extraction_UI).

Monitora i tuoi task GEE in background e invia notifiche istantanee ai tuoi canali preferiti quando terminano, evitando di dover controllare manualmente il Task Manager di GEE.

## 🚀 Funzionalità

- **Notifiche Multi-Canale:**
  - **Telegram:** Messaggi istantanei tramite un Bot Telegram.
  - **Desktop:** Notifiche Windows Toast con logo GEE personalizzato.
  - **Microsoft Teams:** Integrazione Webhook per flussi di lavoro professionali.
- **Monitoraggio Durata:** Calcola e visualizza automaticamente quanto tempo ha impiegato ogni task (es. `12m 45s`).
- **Output Pulito:** Si concentra sulla descrizione e sullo stato del task, eliminando l'ID del task per una migliore leggibilità.
- **Modalità Daemon:** Funziona come un processo leggero in background con intervalli di polling personalizzabili.
- **Configurazione Semplice:** Gestito interamente tramite un semplice file `settings.toml`.

## 🛠️ Installazione

1. **Clona il repository** (o vai nella cartella del progetto).
2. **Crea e attiva un ambiente virtuale:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. **Installa le dipendenze:**
   ```powershell
   pip install -r requirements.txt
   ```

## ⚙️ Configurazione

Configura il sistema modificando il file `settings.toml` nella directory principale:

```toml
[gee]
project_id = "asrdownscalingcropdata"
polling_interval_seconds = 60

[telegram]
enabled = true
bot_token = "IL_TUO_BOT_TOKEN"
chat_id = "IL_TUO_CHAT_ID"

[desktop]
enabled = true

[teams]
enabled = false
webhook_url = "IL_TUO_WEBHOOK_URL"
```

### Configurazione Icona Desktop
Il sistema utilizza un'icona personalizzata situata in `assets/favicon.ico`. Se desideri cambiarla, sostituisci semplicemente questo file con il tuo file `.ico`.

## 🏃 Utilizzo

Avvia il sistema di notifica eseguendo:

```powershell
python main.py
```

Lo script inizializzerà l'API di GEE e inizierà a monitorare gli aggiornamenti dei task. Vedrai un log nella console ogni volta che un task cambia stato.

## 📁 Struttura del Progetto

- `gee_notify/`: Pacchetto principale contenente la logica di monitoraggio e notifica.
- `assets/`: Contiene l'icona delle notifiche.
- `settings.toml`: La tua configurazione locale.
- `main.py`: Il punto di ingresso dell'applicazione.

## 📄 Licenza

MIT

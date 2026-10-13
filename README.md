# GEE Notify

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Earth Engine](https://img.shields.io/badge/GEE-Earth--Engine-green.svg)](https://earthengine.google.com/)

<!-- language-selector -->
[English](README.md) | [Italiano](README.it.md)
<!-- language-selector-end -->

A professional notification system for **Google Earth Engine (GEE)**. This tool was specifically developed as a companion for the [GEE Data Extraction UI](https://github.com/Mastro1/GEE_data_extraction_UI) project.

It monitors your GEE tasks in the background and sends instant notifications to your preferred channels when they finish, so you don't have to check the GEE Task Manager manually.

## 🚀 Features

- **Multi-Channel Notifications:**
  - **Telegram:** Instant messages via a Telegram Bot.
  - **Desktop:** Windows Toast notifications with a custom GEE logo.
  - **Microsoft Teams:** Webhook integration for professional workflows.
- **Duration Tracking:** Automatically calculates and displays how long each task took (e.g., `12m 45s`).
- **Clean Output:** Focuses on the task description and status, removing unnecessary Task ID clutter.
- **Daemon Mode:** Runs as a lightweight background process with customizable polling intervals.
- **Easy Configuration:** Managed entirely via a simple `settings.toml` file.

## 🛠️ Installation

1. **Clone the repository** (or navigate to your project folder).
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Configure the system by editing the `settings.toml` file in the root directory:

```toml
[gee]
project_id = "mygeeproject"
polling_interval_seconds = 60

[telegram]
enabled = true
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

[desktop]
enabled = true

[teams]
enabled = false
webhook_url = "YOUR_WEBHOOK_URL"
```

### Desktop Icon Setup
The system uses a custom icon located in `assets/favicon.ico`. If you want to change it, simply replace this file with your own `.ico` icon.

## 🏃 Usage

Start the notification daemon by running:

```powershell
python main.py
```

The script will initialize the GEE API and start polling for task updates. You will see a log in the console whenever a task changes state.

## 📁 Project Structure

- `gee_notify/`: Main package containing the monitoring and notification logic.
- `assets/`: Contains the notification icon.
- `settings.toml`: Your local configuration.
- `main.py`: The entry point for the application.

## 📄 License

MIT

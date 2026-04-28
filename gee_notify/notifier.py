import requests
import logging
import os
import ctypes

# This tells Windows to treat this process as a unique app, not just 'python.exe'
# It helps in changing the 'Python' text in the notification header.
try:
    myappid = 'Google.EarthEngine.Notify.System.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        if self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN" or not self.bot_token:
            logger.warning("Telegram Bot Token is not configured. Notifications will not be sent.")

    def send_notification(self, message: str, title: str = "GEE Task Update") -> bool:
        """Sends a message to the configured Telegram chat."""
        if self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN" or not self.bot_token:
            logger.error("Cannot send notification: Telegram bot token not configured.")
            return False
            
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            logger.info("Successfully sent Telegram notification.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response details: {e.response.text}")
            return False

class DesktopNotifier:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        if self.enabled and not PLYER_AVAILABLE:
            logger.warning("Desktop notifications are enabled, but 'plyer' is not installed. They will not be sent.")

    def send_notification(self, message: str, title: str = "GEE Task Update") -> bool:
        if not self.enabled:
            return False
        
        if not PLYER_AVAILABLE:
            logger.error("Cannot send desktop notification: 'plyer' package is missing.")
            return False
            
        try:
            # Strip markdown for desktop notification
            clean_message = message.replace("*", "").replace("`", "")
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "favicon.ico"))
            
            try:
                notification.notify(
                    title=title,
                    message=clean_message,
                    app_name="GEE Notify",
                    app_icon=icon_path if os.path.exists(icon_path) else None,
                    timeout=10
                )
            except Exception as icon_e:
                logger.warning(f"Failed to load icon, retrying without icon: {icon_e}")
                notification.notify(
                    title=title,
                    message=clean_message,
                    app_name="GEE Notify",
                    app_icon=None,
                    timeout=10
                )
            logger.info("Successfully sent desktop notification.")
            return True
        except Exception as e:
            logger.error(f"Failed to send desktop notification: {e}")
            return False

class CompositeNotifier:
    def __init__(self, notifiers: list):
        self.notifiers = notifiers

    def send_notification(self, message: str, title: str = "GEE Task Update") -> bool:
        success = False
        for notifier in self.notifiers:
            if notifier.send_notification(message, title):
                success = True
        return success

class TeamsNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        if not self.webhook_url or self.webhook_url == "YOUR_TEAMS_WEBHOOK_URL":
            logger.warning("Teams Webhook URL is not configured. Notifications will not be sent.")

    def send_notification(self, message: str, title: str = "GEE Task Update") -> bool:
        """Sends a message to the configured Microsoft Teams channel."""
        if not self.webhook_url or self.webhook_url == "YOUR_TEAMS_WEBHOOK_URL":
            return False
            
        # Teams uses a simple JSON structure for Message Cards
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0078D7",
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "text": message.replace("*", "**") # Teams uses ** for bold
            }]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logger.info("Successfully sent Teams notification.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Teams notification: {e}")
            return False

import logging
import sys
from gee_notify.config import load_config
from gee_notify.gee_client import initialize_gee
from gee_notify.notifier import TelegramNotifier, DesktopNotifier, CompositeNotifier, TeamsNotifier
from gee_notify.monitor import run_monitor_daemon

# Configure basic logging to output to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def main():
    try:
        # Load configuration
        config = load_config()
        gee_config = config.get("gee", {})
        telegram_config = config.get("telegram", {})
        desktop_config = config.get("desktop", {})
        teams_config = config.get("teams", {})
        
        project_id = gee_config.get("project_id", "asrdownscalingcropdata")
        polling_interval = gee_config.get("polling_interval_seconds", 300)
        
        bot_token = telegram_config.get("bot_token", "")
        chat_id = telegram_config.get("chat_id", "")
        telegram_enabled = telegram_config.get("enabled", True)
        desktop_enabled = desktop_config.get("enabled", False)
        teams_enabled = teams_config.get("enabled", False)
        teams_webhook_url = teams_config.get("webhook_url", "")
        
        # Initialize components
        initialize_gee(project_id)
        
        notifiers = []
        
        # Add Telegram
        if telegram_enabled and bot_token and chat_id:
            notifiers.append(TelegramNotifier(bot_token=bot_token, chat_id=chat_id))
            
        # Add Desktop
        if desktop_enabled:
            notifiers.append(DesktopNotifier(enabled=True))
            
        # Add Teams
        if teams_enabled and teams_webhook_url:
            notifiers.append(TeamsNotifier(webhook_url=teams_webhook_url))
            
        composite_notifier = CompositeNotifier(notifiers)
        
        # Start daemon
        run_monitor_daemon(polling_interval=polling_interval, notifier=composite_notifier)
        
    except Exception as e:
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()

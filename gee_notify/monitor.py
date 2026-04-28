import time
import logging
from datetime import datetime, timedelta
from gee_notify.gee_client import get_recent_tasks

logger = logging.getLogger(__name__)

def format_duration(start_ms, end_ms):
    """Calculates and formats the duration between two millisecond timestamps."""
    if not start_ms or not end_ms:
        return "Unknown"
    
    duration_ms = end_ms - start_ms
    seconds = int((duration_ms / 1000) % 60)
    minutes = int((duration_ms / (1000 * 60)) % 60)
    hours = int((duration_ms / (1000 * 60 * 60)) % 24)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
        
    return " ".join(parts)

def run_monitor_daemon(polling_interval: int, notifier):
    """
    Runs continuously, checking for task state changes.
    """
    logger.info(f"Starting GEE Task Monitor Daemon. Polling every {polling_interval} seconds.")
    
    # Keep track of task states: {task_id: state}
    known_tasks = {}
    
    # Initial load: grab all current tasks so we don't spam notifications for old ones
    initial_tasks = get_recent_tasks()
    for task in initial_tasks:
        task_id = task.get('id')
        state = task.get('state')
        if task_id:
            known_tasks[task_id] = state
            
    logger.info(f"Loaded {len(known_tasks)} existing tasks.")

    while True:
        try:
            time.sleep(polling_interval)
            
            logger.debug("Polling GEE tasks...")
            current_tasks = get_recent_tasks()
            
            for task in current_tasks:
                task_id = task.get('id')
                state = task.get('state')
                description = task.get('description', 'Unknown Task')
                task_type = task.get('task_type', 'Unknown Type')
                
                if not task_id:
                    continue
                
                previous_state = known_tasks.get(task_id)
                
                # If state changed, or it's a new task that immediately completed/failed
                if state != previous_state:
                    logger.info(f"Task '{description}' ({task_id}) changed state: {previous_state} -> {state}")
                    
                    # We are mostly interested in when tasks finish (COMPLETED, FAILED, CANCELLED)
                    if state in ['COMPLETED', 'FAILED', 'CANCELLED'] and previous_state in ['READY', 'RUNNING']:
                        # Calculate duration
                        start_ms = task.get('start_timestamp_ms')
                        update_ms = task.get('update_timestamp_ms')
                        duration_str = format_duration(start_ms, update_ms)

                        # Prepare message
                        status_emoji = "✅" if state == "COMPLETED" else "❌" if state == "FAILED" else "⚠️"
                        msg = (
                            f"{status_emoji} *GEE Task Update*\n"
                            f"*Task:* {description}\n"
                            f"*Type:* {task_type}\n"
                            f"*Status:* {state}\n"
                            f"*Duration:* {duration_str}"
                        )
                        
                        error_msg = task.get('error_message')
                        if error_msg:
                            msg += f"\n*Error:* {error_msg}"
                            
                        # Send notification
                        notifier.send_notification(msg)
                    
                    # Update known state
                    known_tasks[task_id] = state
                    
        except KeyboardInterrupt:
            logger.info("Monitor daemon stopped by user.")
            break
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}")
            time.sleep(60) # Sleep on error before retrying

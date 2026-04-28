import ee
import logging

logger = logging.getLogger(__name__)

def initialize_gee(project_id: str):
    """Initializes the Google Earth Engine API."""
    try:
        ee.Initialize(project=project_id)
        logger.info(f"Successfully initialized GEE for project: {project_id}")
    except Exception as e:
        logger.error(f"Failed to initialize GEE: {e}")
        logger.info("Attempting to authenticate. This may require interactive login.")
        try:
            ee.Authenticate()
            ee.Initialize(project=project_id)
            logger.info(f"Successfully authenticated and initialized GEE for project: {project_id}")
        except Exception as auth_e:
            logger.error(f"Failed to authenticate GEE: {auth_e}")
            raise

def get_recent_tasks() -> list:
    """
    Fetches the list of recent tasks.
    Returns a list of task objects (dictionaries).
    """
    try:
        # ee.data.getTaskList() returns a list of dictionaries with task info
        return ee.data.getTaskList()
    except Exception as e:
        logger.error(f"Error fetching task list: {e}")
        return []

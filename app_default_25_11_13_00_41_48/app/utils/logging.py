from loguru import logger
import sys
from app.config import settings

def configure_logging():
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> | <level>{message}</level>", level=settings.LOG_LEVEL)
    logger.add("logs/backend.log", rotation="10 MB", retention="7 days", compression="zip", level=settings.LOG_LEVEL)

# Instantiate a logger instance for imports
logger = logger

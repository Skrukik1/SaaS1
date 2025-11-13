from loguru import logger
import sys

def configure_bot_logging():
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> | <level>{message}</level>", level="INFO")
    logger.add("logs/bot.log", rotation="10 MB", retention="7 days", compression="zip", level="INFO")

logger = logger

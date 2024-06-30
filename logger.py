import logging
from logging.handlers import RotatingFileHandler
from config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(settings.LOG_LEVEL)

# File handler with rotation
fh = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
fh.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

def log_error_context(e, context=""):
    logger.error(f"{context} - Error: {e}", exc_info=True)

def predict_errors(error_history):
    # Use statistical models to predict and mitigate potential errors
    # Placeholder for actual implementation
    pass

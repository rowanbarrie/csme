import logging

from config import settings

logging.getLogger().setLevel(settings.log_level)

import logging
import logging.config

from .logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)

db_logger = logging.getLogger(name='database')

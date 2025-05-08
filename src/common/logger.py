import logging
import logging.config

from .logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)

root_logger = logging.getLogger('root')

db_logger = logging.getLogger(name='database')
api_logger = logging.getLogger(name='api')

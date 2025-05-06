import logging
from enum import Enum


# short messages is used for faster searching for needed message in loger
class ShortMessages(Enum):

    # auth 1..
    USU = (101, 'user signed up')
    USI = (102, 'user signed in')

    # sessions 2..
    SAS = (201, 'started a session')
    FTS = (202, 'finished the session')
    PTS = (203, 'paused the session')
    CTS = (204, 'continued the session')

    # tags 3..
    CNT = (301, 'created a new tag')


class Logger(logging.Logger):
    '''
    custom logger class for thatrack. extends basic `logging.Logger` class, but with its features
    '''

    __deffault_logger_level = logging.DEBUG
    

    def __init__(self, name, level=__deffault_logger_level):
        """
        Initialize the logger with a name and an optional level.
        """
        logging.Filterer.__init__(self)
        self.name = name
        self.level = logging._checkLevel(level)
        self.parent = None
        self.propagate = True
        self.disabled = False
        self._cache = {}
        
        file_handler = logging.FileHandler("thatrack.log")
        file_handler.setLevel(self.__deffault_logger_level)

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        self.handlers = [file_handler]


    def info(self, short_msg: ShortMessages, msg = '', *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, f'{short_msg.name}  {msg if msg != "" else short_msg.value[1]}', args, **kwargs)
            print(f'{self.name} - {short_msg.name} {msg if msg != "" else short_msg.value[1]}')


db_logger = Logger(name='database')
bot_logger = Logger(name='tgbot')

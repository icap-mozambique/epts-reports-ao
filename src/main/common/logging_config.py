import logging
import logging.config
from src.main.common.file_util import FileUtil

class LoggingConfig:

    def __init__(self, config) -> None:
        self.config = config
    
    def logging_setup(self):
        logging.config.dictConfig(self.config)
        return logging.getLogger(__name__)
'''
logs messages in terminal and in log file
'''
import logging

LOG_FORMAT = "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"

class Logger:
    '''Container for logger'''
    def __init__(self, filename):
        self.filename = filename
        self.logger = logging.getLogger('mars_rover_logger')

        #Create handlers
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename)

        stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def log_info(self, text):
        '''Function for logging [INFO]'''
        self.logger.info(text)

    def log_warn(self, text):
        '''Function for logging [WARNING]'''
        self.logger.warning(text)

    def log_err(self, text):
        '''Function for logging [ERROR]'''
        self.logger.error(text)

import logging
import os
import sys

LOGS_ROOT = "./logs/"

class Log:
    log: logging.Logger = None

    def __init__(self, name="") -> None:
        if Log.log == None:
            Log.log = self._init_logger(name)

    def _init_logger(self, name):
        logger = logging.getLogger(name)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        log_filename = os.path.join(LOGS_ROOT, f"{name}_logger.log")
        file_handler = logging.FileHandler(log_filename, mode="a")
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        return logger




import sys

import os


from loguru import logger


class Logger:
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"

    def __init__(
        self,
        level: str,
        path_directory: str,
        info_log_path: str = None,
        debug_log_path: str = None,
    ):
        self.level = level
        self.path_directory = path_directory
        self.info_log_path = info_log_path
        self.debug_log_path = debug_log_path

    def create_log_directory_if_exists(self):
        if not os.path.exists(self.path_directory):
            os.makedirs(self.path_directory, exist_ok=True)

    def setup_logger(self):
        self.create_log_directory_if_exists()
        match self.level:
            case "debug":
                log_path = self.debug_log_path
            case "info":
                log_path = self.info_log_path
            case _:
                raise ValueError(f"Invalid log level: {self.level}")

        logger.remove()

        logger.add(
            log_path,
            format=self.log_format,
            level=self.level.upper(),
            rotation="500 MB",
            compression="zip",
        )

        logger.add(
            sys.stdout,
            format=self.log_format,
            level=self.level.upper(),
        )

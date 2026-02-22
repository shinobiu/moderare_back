import logging
from logging.handlers import RotatingFileHandler
from core.config import settings
import os


class LoggingConfig:
    @staticmethod
    def setup():
        log_level = logging.DEBUG if settings.ENV.lower() == "development" else logging.INFO

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # garante pasta de logs
        os.makedirs("logs", exist_ok=True)

        file_handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler]
        )

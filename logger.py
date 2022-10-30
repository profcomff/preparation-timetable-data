import logging
from datetime import datetime

_log_file_format = f"%(asctime)s - %(levelname)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_stream_format = f"%(levelname)s - %(message)s"
_file_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S-%f") + ".log"


def _get_file_handler():
    """Файловый обработчик."""
    file_handler = logging.FileHandler(_file_name, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_log_file_format))
    return file_handler


def _get_stream_handler():
    """Потоковый обработчик."""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_stream_format))
    return stream_handler


def get_logger(name):
    """Создает логгер."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_get_file_handler())
    logger.addHandler(_get_stream_handler())
    return logger

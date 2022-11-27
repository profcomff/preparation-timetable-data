import logging

import requests
from requests.exceptions import RequestException
from retrying import retry

from utilities import urls_api

_logger = logging.getLogger(__name__)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def delete_lessons(headers):
    """
    Удаляет все пары из базы данных.
    """
    _logger.info("Удаляю пары из базы данных...")


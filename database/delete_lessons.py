import datetime
import logging

import requests
from requests.exceptions import RequestException
from retrying import retry

from utilities import urls_api

_logger = logging.getLogger(__name__)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def delete_lessons(headers, start, end, base):
    """
    Удаляет все пары из базы данных.
    """
    _logger.info("Удаляю пары из базы данных... ")
    start = datetime.datetime.strptime(start, "%m/%d/%Y")
    end = datetime.datetime.strptime(end, "%m/%d/%Y")

    start = start.timestamp()
    end = end.timestamp()

    url_delete_events = urls_api.get_url_event(urls_api.MODES_URL.delete, base) + 'bulk'
    events = {'start': start, 'end': end}

    r = requests.delete(url_delete_events, json=events, headers=headers)
    _logger.debug(r.json())

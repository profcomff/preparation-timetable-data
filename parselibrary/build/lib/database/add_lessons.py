import logging

import requests
from requests.exceptions import RequestException
from retrying import retry

from utilities import urls_api

_logger = logging.getLogger(__name__)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def upload_event(event, headers, base):
    requests.post(urls_api.get_url_event(urls_api.MODES_URL.post, base), json=event, headers=headers)


def add_lessons(lessons, headers, base):
    """
    Загружает все пары в базу данных.
    """
    _logger.info("Загружаю пары в базу данных...")

    for i, row in lessons.iterrows():
        event = {
            "name": row['subject'],
            "room_id": row['place'],
            "group_id": int(row['group']),
            "lecturer_id": row['teacher'],
            "start_ts": row['start'],
            "end_ts": row['end']
        }
        upload_event(event, headers, base)


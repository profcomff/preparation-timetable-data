import logging
import datetime
import requests
from requests.exceptions import RequestException
from retrying import retry

from profcomff_parse_lib.utilities import urls_api

_logger = logging.getLogger(__name__)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def upload_event(event, headers, base):
    requests.post(urls_api.get_url_event(urls_api.MODES_URL.post, base), json=event, headers=headers)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def post_event(headers, event, base):
    event = {
        "name": event['subject'],
        "room_id": event['place'],
        "group_id": event['group'],
        "lecturer_id": event['teacher'],
        "start_ts": event['start'],
        "end_ts": event['end']
    }
    url = urls_api.get_url_event(urls_api.MODES_URL.post, base)
    r = requests.post(url, json=event, headers=headers).json()
    return r["id"]

def post_events(headers, events):
    r = requests.post("https://api.test.profcomff.com/event/bulk", json=events, headers=headers).json()
    return len(r)


def check_date(event_id, base, begin):
    url = urls_api.get_url_event(urls_api.MODES_URL.get, base)
    r = requests.get(f"{url}{event_id}")
    date_event = r.json()["start_ts"]
    date_event = date_event[:date_event.find("T")]
    date1 = datetime.datetime.strptime(begin, '%m/%d/%Y')
    date2 = datetime.datetime.strptime(date_event, '%Y-%m-%d')
    return date2 >= date1


def add_lessons(lessons, headers, base):
    """
    Загружает все пары в базу данных.
    """
    _logger.info("Загружаю пары в базу данных...")

    for i, row in lessons.iterrows():
        event = {
            "name": row['subject'],
            "room_id": row['place'],
            "group_id": row['group'],
            "lecturer_id": row['teacher'],
            "start_ts": row['start'],
            "end_ts": row['end']
        }
        upload_event(event, headers, base)


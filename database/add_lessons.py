import json
import logging

import requests
import pandas as pd
from requests.exceptions import RequestException
from retrying import retry

from utilities import urls_api

_logger = logging.getLogger(__name__)


# @retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
#        wait_exponential_max=30000, stop_max_attempt_number=30)
def upload_event(event, headers, url_post_event):
    r = requests.post(url=url_post_event, data=event, headers=headers)
    _logger.debug(r.json())


def add_lessons(lessons, headers, base):
    """
    Загружает все пары в базу данных.
    """
    # print(lessons.iloc[0])

    _logger.info("Загружаю пары в базу данных...")
    url_post_event = urls_api.get_url_event(urls_api.MODES_URL.post, base) + 'bulk'
    print(url_post_event)
    lessons.rename(columns={'group': 'group_id', 'subject': 'name', 'place': 'room_id', 'start': 'start_ts', 'end': 'end_ts', 'teacher': 'lecturer_id'}, inplace=True)
    lessons.pop('index')
    # print(lessons.iloc[0])
    # df = pd.DataFrame(columns=['name', 'room_id', 'group_id', 'lecturer_id', 'start_ts', 'end_ts'])
    # for i, row in lessons.iterrows():
    #     event = {
    #         "name": row['subject'],
    #         "room_id": row['place'],
    #         "group_id": int(row['group']),
    #         "lecturer_id": row['teacher'],
    #         "start_ts": row['start'],
    #         "end_ts": row['end']
    #     }
    #     upload_event(event, headers, url_post_event)
    result = lessons.to_json(orient='records', force_ascii=False).encode('utf-8')
    # parsed = json.loads(result)
    # print(json.dumps(parsed, indent=4))
    #
    upload_event(result, headers, url_post_event)


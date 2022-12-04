import logging

import requests

from utilities import urls_api

_logger = logging.getLogger(__name__)


def add_lessons(lessons, headers, base):
    """
    Загружает все пары в базу данных.
    """
    _logger.info("Загружаю пары в базу данных...")

    url_post_event = urls_api.get_url_event(urls_api.MODES_URL.post, base) + 'bulk'
    lessons.rename(
        columns={'group': 'group_id', 'subject': 'name', 'place': 'room_id', 'start': 'start_ts', 'end': 'end_ts',
                 'teacher': 'lecturer_id'}, inplace=True)
    lessons.pop('index')

    result = lessons.to_json(orient='records', force_ascii=False).encode('utf-8')

    r = requests.post(url=url_post_event, data=result, headers=headers)
    _logger.debug(r)

import logging

import pandas as pd

from timetable.core.parse_timetable import parse_timetable

_logger = logging.getLogger(__name__)


def classical_parse_timetable(sources):  # sources: [[курс, поток, количество групп], ...]
    _logger.info("Начинаю парсинг сайта расписания...")

    results = pd.DataFrame()
    for index, source in enumerate(sources):
        for group in range(1, source[2] + 1):
            results = pd.concat([results, parse_timetable(source[0], source[1], group)])

    return results

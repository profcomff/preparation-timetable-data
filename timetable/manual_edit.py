import logging

import pandas as pd

_logger = logging.getLogger(__name__)


def _shell(odd, even, weekday, num, start, end, group, subjects, teacher, place):
    return {"odd": odd, "even": even, "weekday": weekday, "num": num, "start": start, "end": end,
            "group": group, "subject": subjects, "teacher": teacher, "place": place}


deleted_rows = [{"group": "407", "weekday": 4}]

added_rows = pd.DataFrame([
    _shell(True, True, 4, 2, "13:30", "15:05", "407", "КТП", "Мещеряков Н. П.", "1-22а"),
    _shell(True, False, 4, 3, "15:20", "16:55", "407", "КТП", "Мещеряков Н. П.", "1-22а"),
])


def _delete_row(lessons, row):
    """Удаляет строчку/и из DataFrame. См. тест."""
    sub_lessons = lessons
    for key in row.keys():
        sub_lessons = sub_lessons[getattr(sub_lessons, key) == row[key]]

    lessons = lessons.drop(sub_lessons.index)
    return lessons


def manual_edit(lessons):
    """
    Добавляет или удаляет необходимые пары. Пары добавляются вручную.
    """
    _logger.info("Изменяю пары...")

    # Сперва удаляем пары.
    for deleted_row in deleted_rows:
        lessons = _delete_row(lessons, deleted_row)

    # Теперь добавляем.
    lessons = pd.concat([lessons, added_rows], ignore_index=True)

    return lessons



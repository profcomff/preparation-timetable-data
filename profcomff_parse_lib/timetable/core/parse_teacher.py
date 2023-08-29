import logging
import re

import pandas as pd

_logger = logging.getLogger(__name__)


def parse_teacher(lessons):
    """
    Преобразует каждый элемент колонки 'teacher' в элементы вида ['Фамилия И. О.', ...].
    """
    _logger.info("Начинаю парсить 'teacher'...")

    teachers = []
    for index, row in lessons.iterrows():
        teacher = row["teacher"]

        if pd.notna(teacher):
            # TODO: У некоторых преподавателей нет отчества.
            result = re.findall(r"[А-Яа-яёЁ]+ +[А-Яа-яёЁ]\. +[А-Яа-яёЁ]\.", teacher)
            for i, item in enumerate(result):
                item = re.match(r"([А-Яа-яёЁ]+) +([А-Яа-яёЁ]\.) +([А-Яа-яёЁ]\.)", item)
                result[i] = item[1] + " " + item[2] + " " + item[3]

            teacher = result

        if isinstance(teacher, list):
            teacher = tuple(teacher)
        teachers.append(teacher)

    lessons["teacher"] = teachers
    return lessons

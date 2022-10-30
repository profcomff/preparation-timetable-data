import re

import pandas as pd

import logger

_logger = logger.get_logger(__name__)


def _parse_name(name):
    """
    Разделяет одно 'name' на 'subject', 'teacher' и 'place' по заданным регулярным выражениям.
    В случае отсутствия подходящего регулярного выражения ставит 'subject' равным 'name' и выдает предупреждение.
    В 'subject' включен номер группы, если он указан в названии.
    """
    parsed_name = {"subject": None, "teacher": None, "place": None}

    # 4 курс без астр,и 407 - МАТЕМАТИЧЕСКИЕ МОДЕЛИ ФЛУКТУАЦИОННЫХ ЯВЛЕНИЙ <nobr>5-27</nobr> проф. Чиркин А. С.
    result = re.match(r"([А-Яа-яёЁa-zA-Z +,/.\-\d]+)<nobr>([А-Яа-яёЁa-zA-Z +,/.\-\d]+)</nobr>" +
                      r"([А-Яа-яёЁa-zA-Z +,/.\-\d]+)", name)
    if not (result is None):
        if name == result[0]:
            parsed_name["subject"] = result[1]
            parsed_name["place"] = result[2]
            parsed_name["teacher"] = result[3]
            return parsed_name

    # ... <nobr>Каф.</nobr>
    result = re.match(r'([А-Яа-яёЁa-zA-Z +,/.\-\d]+)<nobr>([А-Яа-яёЁa-zA-Z +,/.\-0\d]+)</nobr> *', name)
    if not (result is None):
        if name == result[0]:
            parsed_name["subject"] = result[1]
            parsed_name["place"] = result[2]
            return parsed_name

    # Специальный физический практикум (Андрианов Т. А.){i}
    for i in range(2):
        result = re.match(r"([А-Яа-яёЁa-zA-Z +,/.\-\d]*) ([А-Яа-яёЁa-zA-Z]+ *[А-Яа-яёЁa-zA-Z]\. *[А-Яа-яёЁa-zA-Z]\.)"
                          r" ([А-Яа-яёЁa-zA-Z]+ *[А-Яа-яёЁa-zA-Z]\. *[А-Яа-яёЁa-zA-Z]\.)" * i + " *", name)
        if not (result is None):
            if name == result[0]:
                parsed_name["subject"] = result[1]
                parsed_name["teacher"] = "".join([result[j + 2] + " " for j in range(i + 1)])
                return parsed_name

    # Ядерный практикум
    result = re.match(r'([А-Яа-яёЁa-zA-Z +,/.\-\d]*)', name)
    if not (result is None):
        if name == result[0]:
            parsed_name["subject"] = result[1]
            return parsed_name

    _logger.warn(f"Для '{name}' не найдено подходящее регулярное выражение.")
    return {"subject": name, "teacher": None, "place": None}


def parse_name(lessons):
    """
    Разделяет колонку 'name' на 'subject', 'teacher' и 'place'.
    """
    _logger.info("Начинаю парсить 'name'...")

    parsed_names = []
    for index, row in lessons.iterrows():
        name = row["name"]
        parsed_name = _parse_name(name)
        parsed_names.append(parsed_name)

    lessons = lessons.reset_index(drop=True)
    addition = pd.DataFrame(parsed_names).reset_index(drop=True)
    lessons = pd.concat([lessons, addition], axis=1)
    lessons.drop("name", inplace=True, axis=1)
    return lessons

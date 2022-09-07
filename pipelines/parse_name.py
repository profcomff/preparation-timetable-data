import re

import pandas as pd


def _parse_name(subject):
    parsed_name = {"subject": None, "teacher": None, "place": None}

    result = re.match(
        r"([А-Яа-яёЁa-zA-Z +,/.\-\d]+)<nobr>([А-Яа-яёЁa-zA-Z +,/.\-\d]+)</nobr>([А-Яа-яёЁa-zA-Z +,/.\-\d]+)",
        subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = result[1]
            parsed_name["place"] = result[2]
            parsed_name["teacher"] = result[3]
            return parsed_name

    # ... <nobr>Каф.</nobr>
    result = re.match(r"([А-Яа-яёЁa-zA-Z +,/.\-0-9]+)<nobr>([А-Яа-яёЁa-zA-Z +,/.\-0-9]+)</nobr> *", subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = result[1]
            parsed_name["place"] = result[2]
            return parsed_name

    # Специальный физический практикум Андрианов Т. А.
    result = re.match(r"Специальный физический практикум ([А-Яа-яёЁa-zA-Z +,/.\-0-9]+) *", subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = "Специальный физический практикум"
            parsed_name["teacher"] = result[1]
            return parsed_name

    # СПЕЦПРАКТИКУМ Бессонов В. О.
    result = re.match(r"СПЕЦПРАКТИКУМ ([А-Яа-яёЁa-zA-Z +,/.\-0-9]+) *", subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = "СПЕЦПРАКТИКУМ"
            parsed_name["teacher"] = result[1]
            return parsed_name

    return {"subject": subject, "teacher": None, "place": None}


def parse_name(lessons):
    """
    Разделяет колонку 'name' на 'subject', 'teacher' и 'place'.
    """
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

import re

import pandas as pd


def _parse_name(subject):
    parsed_name = {"subject": None, "teacher": None, "place": None}

    result = re.match("([А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)<nobr>([А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)</nobr>([А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)", subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = result[1]
            parsed_name["place"] = result[2]
            parsed_name["teacher"] = result[3]
            return parsed_name

    result = re.match("([А-Яа-яёЁ (:).\-0-9]+)", subject)
    if not (result is None):
        if subject == result[0]:
            parsed_name["subject"] = result[1]
            return parsed_name

    return {"subject": subject, "teacher": None, "place": None}



def parse_name(lessons):
    """
    Разделяет колонку 'name' на 'subject', 'teacher' и 'place'.
    """
    # Регулярки запускаются по порядку до тех пор, пока не получится не null.
    decode_patterns = [
        "(?P<subject>[А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)<nobr>(?P<place>[А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)</nobr>(?P<teacher>[А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)",
        "(?P<subject>[А-Яа-яёЁ (:).\-0-9]+)"
    ]

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

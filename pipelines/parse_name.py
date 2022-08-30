import re

import pandas as pd


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
        parsed_name = {"subject": None, "teacher": None, "place": None}

        for regex in decode_patterns:
            results = re.match(regex, name)
            if results is None:
                continue
            else:
                parsed_name.update(results.groupdict())
                break
        parsed_names.append(parsed_name)

    lessons = lessons.reset_index(drop=True)
    addition = pd.DataFrame(parsed_names).reset_index(drop=True)
    lessons = pd.concat([lessons, addition], axis=1)
    lessons.drop("name", inplace=True, axis=1)

    return lessons

import re

import pandas as pd


def parse_group(lessons):
    """
    Делает так, чтобы в одной строчке была написана пара только для одной группы.
    Дополнительно возвращает список групп вида: [{'name': name, 'number': number}, ]
    """
    # Регулярки запускаются по порядку до тех пор, пока не получится не null.
    decode_patterns = [
        "(?P<subject>[А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)<nobr>(?P<place>[А-Яа-яёЁa-zA-Z\+,/\.\-0-9]+)</nobr>(?P<teacher>[А-Яа-яёЁa-zA-Z \+,/\.\-0-9]+)",
        "(?P<subject>[А-Яа-яёЁ (:).\-0-9]+)"
    ]

    unique_group = set()
    for index, row in lessons.iterrows():
        group = row["group"]

        if pd.isna(group):
            continue

        for regex in decode_patterns:
            results = re.match(regex, group)
            if results is None:
                continue
            else:
                parsed_name = results.groupdict()
                break

        lessons[index, "group"] = group

    return lessons, list(unique_group)
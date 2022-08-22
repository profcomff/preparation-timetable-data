import re

import pandas as pd


def parse_group(lessons):
    """
    Делает так, чтобы в одной строчке была написана пара только для одной группы.
    Дополнительно возвращает список групп вида: [{'name': name, 'number': number}, ]
    """
    # Регулярки запускаются по порядку до тех пор, пока не получится не null.
    decode_patterns = [
        "(\d+[А-Яа-яёЁ]*) *- *([А-Яа-яёЁ \.]+)",
        "(\d+)()"
    ]

    groups = []
    new_rows = []
    unique_groups = set()
    for index, row in lessons.iterrows():
        group = row["group"]

        if pd.isna(group):
            continue

        for regex in decode_patterns:
            results = re.findall(regex, group)
            if not results:
                continue
            else:
                group = results
                break

        unique_groups.update(set(group))

        groups.append(group[0][0])
        if len(group) > 1:
            for i in range(1, len(group)):
                groups.append(group[i][0])
                new_rows.append(row)

    lessons = pd.concat([lessons, pd.DataFrame(new_rows)])
    lessons["group"] = groups
    return lessons, list(unique_groups)

import re

import pandas as pd



def _parse_group(group: str):
    name_group = "[А-Яа-яёЁ \.,\-:]"
    number_group = "\d+ {0,1}[А-Яа-яёЁ]*"

    # 112
    result = re.match("(\d+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], "")]

    # 101 ...
    result = re.match(f"(\d+) ({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2])]

    # 303 - ...
    result = re.match(f"({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2])]

    # 303, 304-...
    result = re.match(f"({number_group}),({number_group}) *- *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[3]), (result[2], result[3])]

    # 303 - .../303 - ...
    result = re.match(f"({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4])]

    # 303 - .../303 - .../303 - ...
    result = re.match(f"({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4]), (result[5], result[6])]

    # 101М-каф.теоретической физики101ма - МП Теорет. физика101 мб МП Физика нейтрино143М -каф. физики частиц и космологиии
    result = re.match(f"({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4]), (result[5], result[6]), (result[7], result[8])]

    return [(group, "")]


def parse_group(lessons):
    """
    Парсит колонку 'group' и, если надо, добавляет допольнительные строчки в таблицу.
    Дополнительно возвращает список групп вида: [{'name': name, 'number': number}, ]
    """
    groups = ["" for _ in range(len(lessons.index))]
    new_rows = []
    unique_groups = set()
    for index, row in lessons.iterrows():
        group = row["group"]

        if pd.isna(group):
            continue

        group = _parse_group(group)

        unique_groups.update(set(group))

        groups[index] = group[0][0]
        if len(group) > 1:
            for i in range(1, len(group)):
                groups.append(group[i][0])
                new_rows.append(row)

    lessons = pd.concat([lessons, pd.DataFrame(new_rows)], ignore_index=True)
    lessons["group"] = groups
    return lessons, list(unique_groups)

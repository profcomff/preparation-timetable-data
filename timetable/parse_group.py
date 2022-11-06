import re

import pandas as pd

from utilities import logger

_logger = logger.get_logger(__name__)


def _parse_group(group):
    """
    Парсит одну группу (подробности см. в parse_group) по заданным регулярным выражениям.
    В случае отсутствия подходящего регулярного выражения выдает предупреждение и возвращает '[(group, "")]'.
    """
    name_group = r"[А-Яа-яёЁ \.,\-:]"
    number_group = r"\d{3} {0,1}[А-Яа-яёЁ]*"

    # 112
    result = re.match(r"(\d+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], "")]

    # 101 ...
    result = re.match(rf"(\d+) ({name_group}+)", group)
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

    # ОТДЕЛЕНИЕ ГЕОФИЗИКИ303 - .../303 - .../303 - ...
    result = re.match(f"ОТДЕЛЕНИЕ ГЕОФИЗИКИ({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4]), (result[5], result[6])]

    # АСТРОНОМИЧЕСКОЕ ОТДЕЛЕНИЕ632...633...636-...
    result = re.match(f"АСТРОНОМИЧЕСКОЕ ОТДЕЛЕНИЕ({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4]), (result[5], result[6])]

    # 101М-...101ма - МП ...101 мб МП ...143М -...
    result = re.match(f"({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)"
                      f"/*({number_group}) *-* *({name_group}+)", group)
    if not (result is None):
        if group == result[0]:
            return [(result[1], result[2]), (result[3], result[4]), (result[5], result[6]), (result[7], result[8])]

    _logger.warn(f"Для '{group}' не найдено подходящее регулярное выражение.")
    return [(group, "")]


def _post_processing(group):
    """Post processing. Нужно для дальнейшего анализа."""
    return group[0].replace(" ", "").lower(), group[1]


def parse_group(lessons):
    """
    Парсит колонку 'group' и, если надо, добавляет дополнительные строчки в таблицу.
    Дополнительно возвращает список групп вида: [{'name': name, 'number': number}, ]
    """
    _logger.info("Начинаю парсить 'group'...")

    groups = ["" for _ in range(len(lessons.index))]
    new_rows = []
    unique_groups = set()
    for index, row in lessons.iterrows():
        group = row["group"]

        if pd.isna(group):
            continue

        group = list(map(_post_processing, _parse_group(group)))

        unique_groups.update(set(group))

        # Добавляем в конец новую строку(-и), если групп оказалось несколько.
        groups[index] = group[0][0]
        if len(group) > 1:
            for i in range(1, len(group)):
                groups.append(group[i][0])
                new_rows.append(row)

    lessons = pd.concat([lessons, pd.DataFrame(new_rows)], ignore_index=True)
    lessons["group"] = groups

    return lessons, list(unique_groups)

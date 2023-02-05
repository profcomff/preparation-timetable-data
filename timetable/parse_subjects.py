import logging
import re

_logger = logging.getLogger(__name__)


def _preprocessing(subject):
    """По сути, исправление опечаток в названии пар."""
    if subject == "309, 312 - 312Д/С, 309 С/К по выбору ":
        return "309, 312 - Д/С, 309 С/К по выбору "

    if subject == "118м ДМП об,. 118ма ":
        return "118м, 118ма ДМП об."

    if subject == "103ма - 103М ДМП, 140М по выбору, 103М,140М - ФТД ":
        return "103ма - 103М ДМП, 103М,140М - ФТД "

    return subject


def _compare_groups(group1, group2):
    """Сравнение групп. Этот процесс сложнее, чем '=='."""
    # Group1 уже прошел через _post_processing.
    group2 = group2.replace(" ", "")
    group2 = group2.lower()

    # Возможна ситуация названия пары 307а - ... у 307 группы (3 курс).
    result = re.match(r"\d{3}\D", group2)
    if result is not None:
        # Этот if не сработает, если на конце группы есть две буквы.
        if result[0] == group2:
            return group1 in group2

    return group1 == group2


def _parse_subjects(group, subject):
    """
    Парсит 'subjects' по заданным регулярным выражениям. Возвращает subject, если у группы есть такой предмет,
    в противном случае возвращает None.
    'Group' должно быть пропущено через '_post_processing'.
    В случае отсутствия подходящего регулярного выражения выдает предупреждение и возвращает сам 'subject'.
    """
    number_group = r"\d{3} {0,1}[А-Яа-яёЁ]{0,2}"
    name_subject = r"[А-Яа-яёЁA-Z ./\-]+"
    delimiter = r"[, .и+\-]*"

    subject = _preprocessing(subject)

    # 307{n} - ...
    for i in range(12):
        result = re.match(f"({number_group})" + f"{delimiter}({number_group})" * i + f" *-* ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if not any([_compare_groups(group, result[1 + j]) for j in range(i + 1)]):
                    return None
                else:
                    return result[1 + i + 1]

    # 307{n} - ..., 302{m} - ...
    for i in range(8):
        for j in range(8):
            result = re.match(f"({number_group})" + f"{delimiter}({number_group})" * i + f" *-* ({name_subject}), *" +
                              f"({number_group})" + f"{delimiter}({number_group})" * j + f" *-* ({name_subject})",
                              subject)
            if not (result is None):
                if subject == result[0]:
                    left = any([_compare_groups(group, result[1 + k]) for k in range(i + 1)])
                    right = any([_compare_groups(group, result[1 + i + 1 + 1 + k]) for k in range(j + 1)])

                    if left:
                        return result[1 + i + 1]
                    elif right:
                        return result[1 + i + 1 + 1 + j + 1]
                    else:
                        return None

    # TODO - сделать [307{n_i} - ...]{m}
    # 307{n} - ..., 302{m} - ..., 308{m} - ...
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result = re.match(
                    f"({number_group})" + f"{delimiter}({number_group})" * i + f" *-* ({name_subject}), *" +
                    f"({number_group})" + f"{delimiter}({number_group})" * j + f" *-* ({name_subject}), *" +
                    f"({number_group})" + f"{delimiter}({number_group})" * k + f" *-* ({name_subject})",
                    subject)
                if not (result is None):
                    if subject == result[0]:
                        left = any([_compare_groups(group, result[1 + l]) for l in range(i + 1)])
                        middle = any([_compare_groups(group, result[1 + i + 1 + 1 + l]) for l in range(j + 1)])
                        right = any([_compare_groups(group, result[1 + i + 1 + 1 + j + 1 + 1 + l]) for l in range(k + 1)])

                        if left:
                            return result[1 + i + 1]
                        elif middle:
                            return result[1 + i + 1 + 1 + j + 1]
                        elif right:
                            return result[1 + i + 1 + 1 + j + 1 + 1 + k + 1]
                        else:
                            return None

    # 1 поток без 307 группы - S
    result = re.match(f"1 поток без [34]07 группы - ({name_subject})", subject)
    if not (result is None):
        if subject == result[0]:
            if any([_compare_groups(group, _group) for _group in ["307", "407"]]):
                return None
            else:
                return result[1]

    # 1 поток без 307 группы и астр. - S
    result = re.match(rf"1 поток без [34]07 группы,* *и астр\.* - ({name_subject})", subject)
    if not (result is None):
        if subject == result[0]:
            if any([_compare_groups(group, _group) for _group in ["307", "407", "301", "401"]]):
                return None
            else:
                return result[1]

    # 4 курс без астр, и 407 - S
    result = re.match(rf"[34] курс без астр\.*,* *и [34]07 - ({name_subject})", subject)
    if not (result is None):
        if subject == result[0]:
            if any([_compare_groups(group, _group) for _group in ["307", "407", "301", "401"]]):
                return None
            else:
                return result[1]

    # Механика
    result = re.match(f"({name_subject})", subject)
    if not (result is None):
        if subject == result[0]:
            return result[1]

    # 15.10-18.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ
    result = re.match(r"(15\.10 *- *18\.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ)", subject)
    if not (result is None):
        if subject == result[0]:
            return result[1]

    _logger.warning(f"Для '{subject}' не найдено подходящее регулярное выражение.")
    return subject


def parse_subjects(lessons):
    """
    Парсит колонку 'subject' и, если надо, удаляет строчку из таблицы (если в названии предметы указаны группы).
    """
    _logger.info("Начинаю парсить 'subjects'...")

    subjects = []
    deleted_rows = []
    for index, row in lessons.iterrows():
        subject = row["subject"]

        subject = _parse_subjects(row["group"], subject)
        if subject is None:
            deleted_rows.append(index)
        else:
            subjects.append(subject)

    lessons.drop(deleted_rows, axis=0, inplace=True)
    lessons["subject"] = subjects
    lessons = lessons.reset_index(drop=True)

    return lessons


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("group")
    parser.add_argument("subject")
    args = parser.parse_args()
    print(_parse_subjects(args.group, args.subject))

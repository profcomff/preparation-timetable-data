import logging
import re
from profcomff_parse_lib.utilities.ndim_iterator import NDimIterator

_logger = logging.getLogger(__name__)


def _preprocessing(subject):
    """По сути, исправление опечаток в названии пар."""
    if subject == "105М, 106М, 110М, 141М - 105МДМП, 106М, 141М, 110М с/к по выб ":
        return "105М, 106М, 110М, 141М - 105М ДМП, 106М, 141М, 110М с/к по выб "

    if subject == "137Мпо выбору, 237мб обяз. ДМП ":
        return "137М по выбору, 237мб обяз. ДМП "

    if subject == "201Мобяз, 207мб по выбору ДМП ":
        return "201М обяз, 207мб по выбору ДМП "

    if subject == "216Ма, 221М - 216мА ДМП,С/К по выбору 221м ":
        return "216Ма, 221М - 216мА ДМП, 221м С/К по выбору"

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


def _parse_subjects(group, subject, is_dash=False):
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

    # [307{value_i} - ...]{dim}
    for dim in range(3):
        for iters in NDimIterator(dim+1, [12, 8, 2][dim]):
            regex = ""
            for i, value in enumerate(iters):
                regex += f"({number_group})" + f"({delimiter})({number_group})" * value + f" *-* ({name_subject})"
                if i != len(iters)-1:
                    regex += ", *"
            result = re.match(regex, subject)
            if not (result is None):
                if subject == result[0]:
                    groups = []     # Example: [["101", "203"], ["434", "342"], ["102"]]
                    subjects_index = []

                    current_index = 0
                    for value in iters:
                        current_groups = []

                        # First group.
                        current_index += 1
                        current_groups.append(result[current_index])

                        # Other groups.
                        for i in range(value):
                            # Delimiter.
                            current_index += 1
                            if is_dash:
                                # Нужно учесть: 402 - 406 == 402, 403, 404, 405, 406
                                if result[current_index].strip().rstrip() == "-":
                                    # Если будет 102м - 103мб, то будет ошибка, поэтому кикаем это.
                                    if result[current_index-1].strip().rstrip().isdigit() \
                                            and result[current_index+1].strip().rstrip().isdigit():
                                        for sub_group in range(int(result[current_index-1])+1, int(result[current_index+1])):
                                            # Не берем первую (уже взяли) и последнюю (возьмем потом).
                                            current_groups.append(str(sub_group))
                            # Group.
                            current_index += 1
                            current_groups.append(result[current_index])

                        # Subject.
                        current_index += 1
                        subjects_index.append(current_index)

                        # Add.
                        groups.append(current_groups)

                    # Handle.
                    groups = list(map(lambda x: any([_compare_groups(group, _x) for _x in x]), groups))
                    if groups.count(True) == 0:
                        return None
                    else:
                        return result[subjects_index[groups.index(True)]]

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

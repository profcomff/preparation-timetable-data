import re


def parse_subjects(lessons):
    """
    Парсит колонку 'subject' и, если надо, удаляет строчку из таблицы (если в названии предметы указаны группы).
    Дополнительно возвращает список предметов.
    """
    number_group = "\d+[А-Яа-яёЁ]*"
    name_subject = "[А-Яа-яёЁA-Z \./\-]+"


    subjects = []
    deleted_rows = []
    for index, row in lessons.iterrows():
        subject = row["subject"]

        # 307 - S
        result = re.match(f"({number_group}) - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] != result[1]:
                    deleted_rows.append(index)
                else:
                    subjects.append(result[2])
                continue

        # 307, 302 - S
        result = re.match(f"({number_group})[, +]*({number_group}) - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] != result[1] and row["group"] != result[2]:
                    deleted_rows.append(index)
                else:
                    subjects.append(result[3])
                continue

        # 307, 302, 306 - S
        result = re.match(f"({number_group})[, +]*({number_group})[, +]*({number_group}) - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] != result[1] and row["group"] != result[2] and row["group"] != result[3]:
                    deleted_rows.append(index)
                else:
                    subjects.append(result[4])
                continue

        # 307 - S, 302 - S
        result = re.match(f"({number_group}) - ({number_group}), ({number_group}) - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] == result[1]:
                    subjects.append(result[2])
                elif row["group"] == result[3]:
                    subjects.append(result[4])
                else:
                    deleted_rows.append(index)
                continue

        # 307 S, 302 S
        result = re.match(f"({number_group}) ({number_group}), ({number_group}) ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] == result[1]:
                    subjects.append(result[2])
                elif row["group"] == result[3]:
                    subjects.append(result[4])
                else:
                    deleted_rows.append(index)
                continue

        # 1 поток без 307 группы - S
        result = re.match(f"1 поток без [34].07 группы - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] == "307" or row["group"] == "407":
                    deleted_rows.append(index)
                else:
                    subjects.append(result[1])
                continue

        # 1 поток без 307 группы и астр. - S
        result = re.match(f"1 поток без [34].07 группы,* *и астр. - ({name_subject})", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] == "307" or row["group"] == "301" or row["group"] == "401":
                    deleted_rows.append(index)
                else:
                    subjects.append(result[1])
                continue

        # 306
        result = re.match(f"({number_group}) *", subject)
        if not (result is None):
            if subject == result[0]:
                if row["group"] != result[1]:
                    deleted_rows.append(index)
                else:
                    subjects.append(result[1])
                continue

        subjects.append(subject)

    lessons.drop(deleted_rows, axis=0, inplace=True)
    lessons["subject"] = subjects
    lessons = lessons.reset_index()

    # Уборка некоторого мусора.
    teachers = []
    subjects = []
    for index, row in lessons.iterrows():
        if "Специальный физический практикум" in row["subject"]:
            result = "".join(re.findall("[А-Яа-яёЁ]+ [А-Яа-яёЁ]{1}\. [А-Яа-яёЁ]{1}\.", row["subject"]))
            if result:
                subjects.append("Специальный физический практикум")
                teachers.append("".join(re.findall("[А-Яа-яёЁ]+ [А-Яа-яёЁ]{1}\. [А-Яа-яёЁ]{1}\.", row["subject"])))
                continue

        teachers.append(row["teacher"])
        subjects.append(row["subject"])

    lessons["teacher"] = teachers
    lessons["subject"] = subjects

    return lessons, list(set(lessons["subject"].tolist()))

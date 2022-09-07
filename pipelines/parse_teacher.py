import re

import pandas as pd


def parse_teacher(lessons):
    """
    Преобразует каждый элемент колонки 'teacher' в элементы вида ['Фамилия И. О.', ...]
    и возвращает список всех уникальных преподавателей.
    """

    teachers = []
    unique_teachers = set()
    for index, row in lessons.iterrows():
        teacher = row["teacher"]

        if pd.notna(teacher):
            teacher = re.findall(r"[А-Яа-яёЁ]+ [А-Яа-яёЁ]\. [А-Яа-яёЁ]\.", teacher)
            unique_teachers.update(set(teacher))

        teachers.append(teacher)
    lessons["teacher"] = teachers
    return lessons, list(unique_teachers)

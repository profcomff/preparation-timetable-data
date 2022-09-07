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
            teacher = re.findall("[А-Яа-яёЁ]+ +[А-Яа-яёЁ]{1}\. +[А-Яа-яёЁ]{1}\.", teacher)
            for i, _teacher in enumerate(teacher):
                _teacher = re.match("([А-Яа-яёЁ]+) +([А-Яа-яёЁ]{1}\.) +([А-Яа-яёЁ]{1}\.)", _teacher)
                _teacher = _teacher[1] + " " + _teacher[2] + " " + _teacher[3]
                teacher[i] = _teacher
            unique_teachers.update(set(teacher))

        teachers.append(teacher)
    lessons["teacher"] = teachers
    return lessons, list(unique_teachers)

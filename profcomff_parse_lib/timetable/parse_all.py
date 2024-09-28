from .core import *


def parse_all(lessons):
    """
    Делает весь необходимый парсинг.
    """
    lessons, places = parse_place(lessons)
    lessons, groups = parse_group(lessons)
    lessons, teachers = parse_teacher(lessons)
    lessons = parse_subjects(lessons)
    lessons, subjects = pretty_subjects(lessons)
    return lessons, places, groups, teachers, subjects
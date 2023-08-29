from .core import *


def parse_all(lessons, dict_substitutions={}):
    """
    Делает весь необходимый парсинг.

    :param: dict_substitutions Смотрите код функции для понимания. 
    """
    lessons, places = parse_place(lessons)
    lessons, groups = parse_group(lessons)
    lessons, teachers = parse_teacher(lessons)
    lessons = parse_subjects(lessons, dict_substitutions.get("parse_subjects", {}))
    lessons, subjects = pretty_subjects(lessons, dict_substitutions.get("pretty_subjects", {}))

    return lessons, places, groups, teachers, subjects

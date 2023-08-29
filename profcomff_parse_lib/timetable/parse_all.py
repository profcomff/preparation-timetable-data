from .core import *
from .flatten import flatten_to_list


def parse_all(lessons, dict_substitutions={}):
    """
    Делает весь необходимый парсинг.

    :param: dict_substitutions Смотрите код функции для понимания. 
    """
    lessons = parse_place(lessons, dict_substitutions.get("parse_place", {}))
    lessons, groups = parse_group(lessons)
    lessons = parse_teacher(lessons)
    lessons = parse_subjects(lessons, dict_substitutions.get("parse_subjects", {}))
    lessons = pretty_subjects(lessons, dict_substitutions.get("pretty_subjects", {}))
    lessons = replace_lessons(lessons, dict_substitutions.get("replace_lessons", {}))

    return (lessons, list(set(lessons["place"].tolist())), groups, 
            list(set(flatten_to_list(lessons["teacher"].tolist()))), 
            list(set(lessons["subject"].tolist())))

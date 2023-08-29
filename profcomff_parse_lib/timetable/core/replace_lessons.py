import logging
import sys

_logger = logging.getLogger(__name__)


def replace_lessons(lessons, substitutions):
    """Меняет пары на нужные."""
    _logger.info("Начинаю менять пары на нужные...")

    substitutions2lessons = {}
    lessons2substitutions = {}

    for index_substitution, substitution in enumerate(substitutions):
        result = True
        for require in substitution["requires"].keys():
            result = result & (lessons[require] == substitution["requires"][require])
        indexes_lessons = lessons.loc[result].index.tolist()

        for index in indexes_lessons:
            if index in lessons2substitutions:
                lessons2substitutions[index].append(index_substitution)
            else:
                lessons2substitutions[index] = [index_substitution]

        if index_substitution in substitutions2lessons:
            substitutions2lessons[index_substitution] += indexes_lessons
        else:
            substitutions2lessons[index_substitution] = indexes_lessons

    flag = False
    for key in substitutions2lessons.keys():
        if len(substitutions2lessons[key]) > 1:
            flag = True
            _logger.critical(f"Замене под номером {key} соответствует количество пар, равному {len(substitutions2lessons[key])}.")

    for key in lessons2substitutions.keys():
        if len(lessons2substitutions[key]) > 1:
            flag = True
            _logger.critical(f"Одной паре соответствует замены под номерами {lessons2substitutions[key]}.")
    
    if flag:
        _logger.critical("Конец программы.")
        sys.exit()
    
    
     
    return lessons

import logging

_logger = logging.getLogger(__name__)


def _preprocessing(subject):
    """Preprocessing."""
    subject = subject.strip()
    subject = subject.rstrip()
    return subject


def pretty_subjects(lessons, dict_substitutions):
    """Превращает название пары в более менее нормальные. Дополнительно возвращает список предметов."""
    _logger.info("Начинаю делать 'subject' красивыми...")

    subjects = lessons["subject"].tolist()
    for i, subject in enumerate(subjects):
        subject = _preprocessing(subject)
        subject = dict_substitutions.get(subject, subject)
        subjects[i] = subject

    lessons["subject"] = subjects
    return lessons, list(set(lessons["subject"].tolist()))

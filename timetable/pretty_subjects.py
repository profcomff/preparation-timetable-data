import logging

# Красивые предметы.
_pretty_subjects = {"Д/п": "Д/П", "С/К по выбору-": "С/К по выбору", "С/К по выбоу": "С/К по выбору",
                    "С/к по выбору": "С/К по выбору", "С/к": "С/К", "Д/С.": "Д/С", "с/к по выбору": "С/К по выбору"}

_logger = logging.getLogger(__name__)


def _preprocessing(subject):
    """Preprocessing."""
    subject = subject.strip()
    subject = subject.rstrip()
    return subject


def pretty_subjects(lessons):
    """Превращает название пары в более менее нормальные. Дополнительно возвращает список предметов."""
    _logger.info("Начинаю делать 'subject' красивыми...")

    # TODO: Убрать капс.
    subjects = lessons["subject"].tolist()
    for i, subject in enumerate(subjects):
        subject = _preprocessing(subject)
        subject = _pretty_subjects.get(subject, subject)
        subjects[i] = subject

    lessons["subject"] = subjects
    return lessons, list(set(lessons["subject"].tolist()))

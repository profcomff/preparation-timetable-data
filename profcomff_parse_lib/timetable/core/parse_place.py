import logging

_logger = logging.getLogger(__name__)


def parse_place(lessons, dict_substitutions):
    """
    На данный момент только меняет название 'place', если оно есть в словаре изменения названий.
    """
    _logger.info("Начинаю парсить 'place'...")

    places = lessons["place"].tolist()
    for i, place in enumerate(places):
        place = dict_substitutions.get(place, place)
        places[i] = place

    lessons["place"] = places
    return lessons

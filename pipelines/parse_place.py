def parse_place(lessons):
    """
    Никак не меняет lessons. Дополнительно возвращает список кабинетов.
    """
    return lessons, list(set(lessons["place"].tolist()))

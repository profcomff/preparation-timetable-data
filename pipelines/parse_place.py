def parse_place(lessons):
    """
    Никак не меняет lessons. Дополнительно возвращает список кабинетов.
    """
    places = lessons["place"].tolist()
    for i, place in enumerate(places):
        if place == "Ауд. им. Хохлова":
            place = "ЦФА"

        places[i] = place

    lessons["place"] = places

    return lessons, list(set(places))

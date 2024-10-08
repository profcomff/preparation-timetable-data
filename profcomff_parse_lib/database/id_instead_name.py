import logging
import sys

import requests

from profcomff_parse_lib.utilities import urls_api

_logger = logging.getLogger(__name__)


def room_to_id(lessons, headers, base):
    """
    Превращает названия комнат в расписании в id для базы данных.
    """
    _logger.info("Превращаю названия комнат в id...")

    response = requests.get(urls_api.get_url_room(urls_api.MODES_URL.get, base), headers=headers)
    rooms = response.json()["items"]

    place = lessons["place"].tolist()
    for i, row in lessons.iterrows():
        for k, ob in enumerate(row["place"]):
            b = False
            for room in rooms:
                if ob == room["name"]:
                    place[i][k] = room["id"]
                    b = True
                    break
            if not b:
                # @mixx3 мы согласны на потери данных в таком случае
                # _logger.critical("Ошибка, аудитория '{aud}' не найдена. Завершение работы".format(aud=row['place']))
                # sys.exit()
                _logger.info("Ошибка, аудитория '{aud}' не найдена. ".format(aud=row['place']))
                place[i][k] = -100  # чтобы не было ошибок в связях
    lessons["place"] = place
    return lessons


def group_to_id(lessons, headers, base):
    """
    Превращает названия групп в расписании в id для базы данных.
    """
    _logger.info("Превращаю названия групп в id...")

    response = requests.get(urls_api.get_url_group(urls_api.MODES_URL.get, base), headers=headers)
    groups = response.json()["items"]

    new_groups = lessons["group"].tolist()
    for i, row in lessons.iterrows():
        for j in range(len(row["group"])):
            b = False
            for group in groups:
                if row["group"][j] == group["number"]:
                    new_groups[i][j] = group["id"]
                    b = True
                    break
            if not b:
                body = {"name": f"Группа # {row['group'][j]}", 'number': row['group'][j]}
                response = requests.request(urls_api.get_url_group(urls_api.MODES_URL.post, base), headers=headers, json=body)
                new_groups[i][j] = response.json()["id"]
                _logger.info(f'Новая группа: {response}')
    lessons["group"] = new_groups

    return lessons


def teacher_to_id(lessons, headers, base):
    """
    Превращает препов в расписании в id для базы данных.
    """
    _logger.info("Превращаю преподавателей в id...")

    response = requests.get(urls_api.get_url_lecturer(urls_api.MODES_URL.get, base), headers=headers)
    teachers = response.json()["items"]

    new_teacher = lessons["teacher"].tolist()
    for i, row in lessons.iterrows():
        for j, item_ in enumerate(row["teacher"]):
            b = False
            for teacher in teachers:
                item = item_.split()
                b1 = item[0] == teacher['last_name']
                b2 = item[1][0] == teacher['first_name'][0]
                b3 = item[2][0] == teacher['middle_name'][0]
                b = b1 and b2 and b3
                if b:
                    new_teacher[i][j] = teacher["id"]
                    break
            if not b:
                item = item_.split()
                body = {"first_name": item[1][0], "middle_name": item[2][0], "last_name": item[0], "description": "Преподаватель физического факультета" }
                response = requests.request(urls_api.get_url_lecturer(urls_api.MODES_URL.post, base), headers=headers,
                                            json=body)
                new_teacher[i][j] = response.json()["id"]
                _logger.info(f'Новый преподаватель: {response}')
    lessons["teacher"] = new_teacher

    return lessons


def to_id(lessons, headers, base):
    lessons = room_to_id(lessons, headers, base)
    lessons = group_to_id(lessons, headers, base)
    lessons = teacher_to_id(lessons, headers, base)
    return lessons

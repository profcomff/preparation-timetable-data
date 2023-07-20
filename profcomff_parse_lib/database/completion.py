import logging

import pandas as pd
import requests

from utilities import urls_api

_logger = logging.getLogger(__name__)


def completion_lecturers(new_lecturers, headers, base):
    """
    Добавляет лекторов в базу данных, которые появляются при парсинге, но в данный момент отсутсвуют в базе.
    """
    _logger.info("Дополняю лекторов...")

    response = requests.get(urls_api.get_url_lecturer(urls_api.MODES_URL.get, base), headers=headers)
    old_lecturers = response.json()["items"]
    new_lecturers = list(map(lambda x: x.split(), new_lecturers))
    url_post_lecturer = urls_api.get_url_lecturer(urls_api.MODES_URL.post, base)

    b = False
    for new_lecturer in new_lecturers:
        for old_lecturer in old_lecturers:
            b1 = new_lecturer[0] == old_lecturer['last_name']
            b2 = new_lecturer[1][0] == old_lecturer['first_name'][0]
            b3 = new_lecturer[2][0] == old_lecturer['middle_name'][0]
            b = b1 and b2 and b3
            if b:
                break

        if not b:
            last_name = new_lecturer[0]
            first_name = new_lecturer[1]
            middle_name = new_lecturer[2]
            data = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name}
            r = requests.post(url_post_lecturer, json=data, headers=headers)
            _logger.debug(r.json())


def completion_rooms(new_rooms, headers, base):
    """
    Добавляет аудитории в базу данных, которые появляются при парсинге, но в данный момент отсутсвуют в базе.
    """
    _logger.info("Дополняю аудитории...")

    response = requests.get(urls_api.get_url_room(urls_api.MODES_URL.get, base), headers=headers)
    old_rooms = response.json()["items"]
    url_post_room = urls_api.get_url_room(urls_api.MODES_URL.post, base)

    b = False
    for new_room in new_rooms:
        for old_room in old_rooms:
            b = new_room == old_room['name']
            if b:
                break

        if not b:
            name = new_room
            if pd.notna(name):
                data = {'name': name, 'direction': None}
                response = requests.post(url_post_room, json=data, headers=headers)
                _logger.debug(response.json())


def completion_groups(new_groups, headers, base):
    """
    Добавляет группы в базу данных, которые появляются при парсинге, но в данный момент отсутсвуют в базе.
    """
    _logger.info("Дополняю группы...")

    response = requests.get(urls_api.get_url_group(urls_api.MODES_URL.get, base), headers=headers)
    old_groups = response.json()["items"]
    url_post_group = urls_api.get_url_group(urls_api.MODES_URL.post, base)

    b = False
    for new_group in new_groups:
        for old_group in old_groups:
            b = new_group[0] == old_group['number']
            if b:
                break

        if not b:
            number = new_group[0]
            name = new_group[1]
            data = {'name': name, 'number': number}
            response = requests.post(url_post_group, json=data, headers=headers)
            _logger.debug(response.json())


def completion(new_groups, new_rooms, new_lecturers, headers, base):
    """
    Добавляет группы, аудитории и лекторов в базу данных, которые появляются при парсинге,
    но в данный момент отсутсвуют в базе.
    """
    completion_lecturers(new_lecturers, headers, base)
    completion_rooms(new_rooms, headers, base)
    completion_groups(new_groups, headers, base)


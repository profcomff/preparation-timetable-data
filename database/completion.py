import logging

import pandas as pd
import requests

from utilities import urls_api as au

_logger = logging.getLogger(__name__)


def completion_lecturers(new_lecturers, headers):
    response = requests.get(au.get_url_lecturer(au.MODES_URL.get), headers=headers)
    # print(au.get_url_lecturer(au.MODES_URL.get))
    # print(response.json())
    # print(headers)
    old_lecturers = response.json()["items"]
    new_lecturers = list(map(lambda x: x.split(), new_lecturers))

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
            requests.post(au.get_url_lecturer(au.MODES_URL.post), json=data, headers=headers)


def completion_rooms(new_rooms, headers):
    # print("COMPLETION_ROOMS", headers)
    response = requests.get(au.get_url_room(au.MODES_URL.get), headers=headers)
    # print(response)
    old_rooms = response.json()["items"]

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
                r = requests.post(au.get_url_room(au.MODES_URL.post), json=data, headers=headers)
                _logger.debug(r.json())
                # print(name, r)


def completion_groups(new_groups, headers):
    response = requests.get(au.get_url_group(au.MODES_URL.get), headers=headers)
    old_groups = response.json()["items"]

    # print(new_groups)
    b = False
    for new_group in new_groups:
        for old_group in old_groups:
            b = new_group[0] == old_group['number']
            if b:
                # print(old_group['number'])
                break

        if not b:
            number = new_group[0]
            name = new_group[1]
            data = {'name': name, 'number': number}
            requests.post(au.get_url_group(au.MODES_URL.post), json=data, headers=headers)


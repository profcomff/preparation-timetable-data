import json

import pandas as pd
import requests

# url = f"https://timetable.api.profcomff.com"
# beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})
# access_token = beaver.json().get("access_token")
# auth_data = json.loads(beaver.content)
# header = {"Authorization": f"Bearer {access_token}"}
#
# url_get_lecturer = f'https://timetable.api.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details' \
#                    f'=description '
# url_post_lecturer = f'https://timetable.api.profcomff.com/timetable/lecturer/'
#
# url_get_room = f'https://timetable.api.profcomff.com/timetable/room/?limit=1000&offset=0'
# url_post_room = f'https://timetable.api.profcomff.com/timetable/room/'
#
# url_get_group = f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0'
# url_post_group = f'https://timetable.api.profcomff.com/timetable/group/'

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
access_token = beaver.json().get("access_token")
auth_data = json.loads(beaver.content)
header = {"Authorization": f"Bearer {access_token}"}

url_get_lecturer = f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details' \
                   f'=description '
url_post_lecturer = f'https://timetable.api.test.profcomff.com/timetable/lecturer/'

url_get_room = f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0'
url_post_room = f'https://timetable.api.test.profcomff.com/timetable/room/'

url_get_group = f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0'
url_post_group = f'https://timetable.api.test.profcomff.com/timetable/group/'

def completion_lecturers(new_lecturers):
    response = requests.get(url_get_lecturer, headers=header)
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
            requests.post(url_post_lecturer, json=data, headers=header)


def completion_rooms(new_rooms):
    response = requests.get(url_get_room, headers=header)
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
                requests.post(url_post_room, json=data, headers=header)

def completion_groups(new_groups):
    response = requests.get(url_get_group, headers=header)
    old_groups = response.json()["items"]

    addition = []
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
            requests.post(url_post_group, json=data, headers=header)
            # addition.append(number)
    # return addition
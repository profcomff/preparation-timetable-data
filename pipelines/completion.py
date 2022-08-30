import json

import pandas as pd
import requests

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
auth_data = json.loads(beaver.content)


def completion_lecturers(new_lecturers):
    response = requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details=description',
                            headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
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
            requests.post(f'https://timetable.api.test.profcomff.com/timetable/lecturer/', json=data,
                          headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})


def completion_rooms(new_rooms):
    response = requests.get(f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0',
                            headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
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
                requests.post(f'https://timetable.api.test.profcomff.com/timetable/room/', json=data,
                              headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})


def completion_groups(new_groups):
    response = requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0',
                            headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    old_groups = response.json()["items"]

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
            requests.post(f'https://timetable.api.test.profcomff.com/timetable/group/', json=data,
                          headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})

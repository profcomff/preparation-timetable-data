import json

import pandas as pd
import requests

# url = f"https://timetable.api.profcomff.com"
# beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})
# access_token = beaver.json().get("access_token")
#
# auth_data = json.loads(beaver.content)
#
# header = {"Authorization": f"Bearer {access_token}"}
#
# url_room = f'https://timetable.api.profcomff.com/timetable/room/?limit=1000&offset=0'
# url_group = f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0'
# url_lecturer = f'https://timetable.api.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details=description'

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
access_token = beaver.json().get("access_token")

auth_data = json.loads(beaver.content)

header = {"Authorization": f"Bearer {access_token}"}

url_room = f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0'
url_group = f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0'
url_lecturer = f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details=description'

def room_to_id(lessons):
    response = requests.get(url_room, headers=header)
    rooms = response.json()["items"]

    place = lessons["place"].tolist()
    for i, row in lessons.iterrows():
        for room in rooms:
            if row["place"] == room["name"]:
                place[i] = room["id"]
                break
    lessons["place"] = place

    return lessons


def group_to_id(lessons):
    response = requests.get(url_group, headers=header)
    groups = response.json()["items"]

    new_groups = lessons["group"].tolist()
    for i, row in lessons.iterrows():
        for group in groups:
            if row["group"] == group["number"]:
                new_groups[i] = group["id"]
                break
    lessons["group"] = new_groups
    new_groups = pd.DataFrame(new_groups)
    return lessons


def teacher_to_id(lessons):
    response = requests.get(url_lecturer, headers=header)
    teachers = response.json()["items"]

    new_teacher = lessons["teacher"].tolist()
    for i, row in lessons.iterrows():
        if isinstance(row["teacher"], list):
            for teacher in teachers:
                for j, item in enumerate(row["teacher"]):
                    if isinstance(item, str):
                        item = item.split()
                        b1 = item[0] == teacher['last_name']
                        b2 = item[1][0] == teacher['first_name'][0]
                        b3 = item[2][0] == teacher['middle_name'][0]
                        b = b1 and b2 and b3
                        if b:
                            new_teacher[i][j] = teacher["id"]
    lessons["teacher"] = new_teacher

    return lessons


def to_id(lessons):
    lessons = room_to_id(lessons)
    lessons = group_to_id(lessons)
    lessons = teacher_to_id(lessons)
    return lessons

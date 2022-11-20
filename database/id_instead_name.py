import logging

import requests

from utilities import urls_api as au
import password

# # au.authorization(password.login, password.password)
# url = au.get_url()
# beaver = requests.post(f"{url}/token", {"username": password.login, "password": password.password})
# access_token = beaver.json().get("access_token")
# headers = {"Authorization": f"Bearer {access_token}"}

_logger = logging.getLogger(__name__)


def room_to_id(lessons, headers):
    response = requests.get(au.get_url_room(au.MODES_URL.get), headers=headers)
    rooms = response.json()["items"]

    place = lessons["place"].tolist()
    for i, row in lessons.iterrows():
        for room in rooms:
            if row["place"] == room["name"]:
                place[i] = room["id"]
                break
    lessons["place"] = place

    return lessons


def group_to_id(lessons, headers):
    response = requests.get(au.get_url_group(au.MODES_URL.get), headers=headers)
    groups = response.json()["items"]

    new_groups = lessons["group"].tolist()
    for i, row in lessons.iterrows():
        for group in groups:
            if row["group"] == group["number"]:
                new_groups[i] = group["id"]
                break
    lessons["group"] = new_groups
    return lessons


def teacher_to_id(lessons, headers):
    response = requests.get(au.get_url_lecturer(au.MODES_URL.get), headers=headers)
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


def to_id(lessons, headers):
    lessons = room_to_id(lessons, headers)
    lessons = group_to_id(lessons, headers)
    lessons = teacher_to_id(lessons, headers)
    return lessons

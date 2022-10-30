import requests

import authorization
from authorization import get_url

url_room = get_url() + "/timetable/room/?limit=1000&offset=0"
url_group = get_url() + "/timetable/group/?limit=1000&offset=0"
url_lecturer = get_url() + "/timetable/lecturer/?limit=1000&offset=0&details=description"


def room_to_id(lessons):
    response = requests.get(url_room, headers=authorization.headers)
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
    response = requests.get(url_group, headers=authorization.headers)
    groups = response.json()["items"]

    new_groups = lessons["group"].tolist()
    for i, row in lessons.iterrows():
        for group in groups:
            if row["group"] == group["number"]:
                new_groups[i] = group["id"]
                break
    lessons["group"] = new_groups
    return lessons


def teacher_to_id(lessons):
    response = requests.get(url_lecturer, headers=authorization.headers)
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

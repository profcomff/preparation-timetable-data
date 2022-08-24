import pandas as pd
import requests
import json

from pipelines.ID_instead_name import to_id
from pipelines.completion import completion_lecturers
from pipelines.completion import completion_rooms
from pipelines.completion import completion_groups
from pipelines.parse_group import parse_group
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher

url=f"https://timetable.api.test.profcomff.com"

# Авторизация
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})

# Парсинг ответа
auth_data=json.loads(beaver.content)

r = requests.delete(f'https://timetable.api.test.profcomff.com/timetable/lecturer/6', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
# print(r)

# lessons = parse_timetable()
# lessons = parse_name(lessons)
lessons = pd.read_excel("parsed_lessons_table.xlsx", sheet_name=0)
lessons = lessons.drop(columns=["id"])

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, subjects = parse_subjects(lessons)
lessons, teachers = parse_teacher(lessons)
#
# completion_lecturers(teachers)
# completion_rooms(places)
# completion_groups(groups)
#
# print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())
# print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())
# print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())

# data = {'name': 'sgdhdh', 'number': 'djfj'}
# requests.post(f'https://timetable.api.test.profcomff.com/timetable/group/', json=data,
#                               headers={"Authorization": f"Bearer {auth_data.get('access_token')}"} )
#
# print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())

djfh = to_id(lessons)
print(djfh)




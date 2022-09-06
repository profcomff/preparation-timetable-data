import pandas as pd

from pipelines.add_events import add_lessons
from pipelines.calc_date import calc_date
from pipelines.completion import completion_groups
from pipelines.completion import completion_lecturers
from pipelines.completion import completion_rooms
from pipelines.fix_eng import fix_eng
from pipelines.id_instead_name import to_id, group_to_id
from pipelines.parse_group import parse_group
from pipelines.parse_name import parse_name
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher
from pipelines.parse_timetable import parse_timetable
import requests
import json
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

lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, subjects = parse_subjects(lessons)
lessons, teachers = parse_teacher(lessons)

completion_lecturers(teachers)
completion_rooms(places)
completion_groups(groups)

response = requests.get(url_group, headers=header)
groups = response.json()["items"]
#
# response = requests.get(url_lecturer, headers=header)
# lecturers = response.json()
#
# response = requests.get(url_room, headers=header)
# rooms = response.json()

# print(groups)
# print(lecturers)
# print(rooms)


grou = []
for i in range(len(groups)):
    # if groups[i]['number'] in addition_groups:
    grou.append(groups[i]['id'])

grou = pd.DataFrame(grou)
lessons = to_id(lessons)

lessons = fix_eng(lessons, grou)
# #
# #
# # a.to_excel("5.xlsx", "List")
# #
# #
# #
semester_begin = "09/05/2022"
semester_end = "09/18/2022"

new_lessons = calc_date(lessons, semester_begin, semester_end)
new_lessons.to_excel("Lessons1.xlsx", "List")
add_lessons(new_lessons)

# for i in range(len(groups)):
#     print(groups[i][0])
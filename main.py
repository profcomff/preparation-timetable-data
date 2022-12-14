import json
import logging

import requests

from database import *
from timetable import *
from utilities import *

parser = get_parser()
args = parser.parse_args()

if args.database == "prod":
    input("WARNING: Загрузка на прод. Вы уверены (CTRL+C если нет)?")

base = args.database
root_logger = logger.get_root_logger(logging.DEBUG if args.debug else logging.INFO)

url = urls_api.get_url(base)
beaver = requests.post(f"{url}/token", {"username": args.login, "password": args.password})
auth_data = json.loads(beaver.content)
access_token = beaver.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# ---------------- Parsing ----------------
lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, teachers = parse_teacher(lessons)
lessons, subjects = parse_subjects(lessons)

lessons = multiple_lessons(lessons)
lessons = flatten(lessons)

# ---------------- Loading to server ----------------
completion_lecturers(teachers, headers, base)
completion_rooms(places, headers, base)
completion_groups(groups, headers, base)

lessons = to_id(lessons, headers, base)
lessons = calc_date(lessons, args.begin, args.end)

delete_lessons(headers, args.begin, args.end, base)
add_lessons(lessons, headers, base)

input("Готово. Для продолжения нажмите любую клавишу.")


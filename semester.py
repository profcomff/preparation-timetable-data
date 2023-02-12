import json
import logging

import requests

from database import *
from timetable import *
from timetable.core.parse_name import parse_name
from utilities import *

parser = get_parser()
args = parser.parse_args()

if args.database == "prod":
    input("WARNING: Загрузка на прод. Вы уверены (CTRL+C если нет)?")

root_logger = logger.get_root_logger(logging.DEBUG if args.debug else logging.INFO)

url = urls_api.get_url(args.database)
beaver = requests.post(f"{url}/token", {"username": args.login, "password": args.password})
auth_data = json.loads(beaver.content)
access_token = beaver.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# ---------------- Parsing timetable from site ----------------
# [[курс, поток, количество групп], ...]
sources = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 8],
    [5, 1, 13], [5, 2, 11],
    [6, 1, 11], [6, 2, 10]
]
lessons = classical_parse_timetable(sources)

# ---------------- Parsing ----------------
lessons = parse_name(lessons)
lessons, places, groups, teachers, subjects = parse_all(lessons)
lessons = manual_edit(lessons)
lessons = multiple_lessons(lessons)
lessons = flatten(lessons)
# lessons.to_excel("lessons.xlsx", "1")

# ---------------- Loading to server ----------------
completion(groups, places, teachers, headers, args.database)

lessons = to_id(lessons, headers, args.database)
lessons = calc_date(lessons, args.begin, args.end)

delete_lessons(headers, args.begin, args.end, args.database)
add_lessons(lessons, headers, args.database)

input("Готово. Для продолжения нажмите любую клавишу.")

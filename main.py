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

root_logger = logger.get_root_logger({"info": logging.INFO, "debug": logging.DEBUG}[args.log_level])

url = urls_api.get_url()
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

if args.debug_parse:
    # TODO: Тест парсинга по изначальным данным.
    lessons = calc_date(lessons, args.begin, args.end)
    lessons.to_excel("lessons.xlsx")

# ---------------- Loading to server ----------------
if not args.debug_parse:
    completion_lecturers(teachers, headers)
    completion_rooms(places, headers)
    completion_groups(groups, headers)

    # lessons = id_instead.to_id(lessons, headers)
    # lessons = calc_date(lessons, args.begin, args.end)
    #
    # events.add_lessons(lessons, headers)

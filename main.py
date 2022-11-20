import logging

from timetable import *
from utilities import logger
from utilities.argparser import get_parser

parser = get_parser()
args = parser.parse_args()
if args.database == "prod":
    input("WARNING: Загрузка на прод. Вы уверены (CTRL+C если нет)?")

root_logger = logger.get_root_logger({"info": logging.INFO, "debug": logging.DEBUG}[args.log_level])

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
    pass
    # completion_lecturers(teachers)
    # completion_rooms(places)
    # completion_groups(groups)

    # lessons = to_id(lessons)
    # lessons = calc_date(lessons, args.begin, args.end)

    # add_lessons(lessons)

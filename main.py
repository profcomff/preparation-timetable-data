from timetable import *
from utilities.argparser import get_parser

parser = get_parser()
args = parser.parse_args()
if args.database == "prod":
    input("WARNING: Загрузка на прод. Вы уверены (CTRL+C если нет)?")

# ---------------- Parsing ----------------
lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, teachers = parse_teacher(lessons)
lessons, subjects = parse_subjects(lessons)

# lessons = fix_eng(lessons)

if args.debug:
    # TODO: Тест парсинга по изначальным данным.
    lessons.to_excel("lessons.xlsx")

# ---------------- Loading to server ----------------
if not args.debug:
    pass
    # completion_lecturers(teachers)
    # completion_rooms(places)
    # completion_groups(groups)

    # lessons = to_id(lessons)
    # lessons = calc_date(lessons, args.begin, args.end)

    # add_lessons(lessons)

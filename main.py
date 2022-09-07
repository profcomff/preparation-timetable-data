import authorization
from pipelines.calc_date import calc_date
from pipelines.completion import completion_groups
from pipelines.completion import completion_lecturers
from pipelines.completion import completion_rooms
from pipelines.fix_eng import fix_eng
from pipelines.id_instead_name import to_id
from pipelines.parse_group import parse_group
from pipelines.parse_name import parse_name
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher
from pipelines.parse_timetable import parse_timetable

authorization.authorization("", "")

lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, subjects = parse_subjects(lessons)
lessons, teachers = parse_teacher(lessons)

completion_lecturers(teachers)
completion_rooms(places)
completion_groups(groups)

lessons = to_id(lessons)

lessons = fix_eng(lessons)

semester_begin = "09/05/2022"
semester_end = "09/18/2022"
lessons = calc_date(lessons, semester_begin, semester_end)

# add_lessons(lessons)

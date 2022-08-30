import pandas as pd

from pipelines.add_events import add_lessons
from pipelines.calc_date import calc_date
from pipelines.completion import completion_groups
from pipelines.completion import completion_lecturers
from pipelines.completion import completion_rooms
from pipelines.id_instead_name import to_id
from pipelines.parse_group import parse_group
from pipelines.parse_name import parse_name
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher
from pipelines.parse_timetable import parse_timetable

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
new_lessons = calc_date(lessons)
add_lessons(new_lessons)

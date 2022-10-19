import requests
import pandas as pd
import authorization as au
import password
from pipelines.add_events import add_lessons
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


lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, teachers = parse_teacher(lessons)
lessons, subjects = parse_subjects(lessons)

# groups = pd.DataFrame(groups)
# groups.to_excel('groups.xlsx', 'List')

completion_lecturers(teachers)
completion_rooms(places)
completion_groups(groups)

lessons = to_id(lessons)

lessons = fix_eng(lessons)

semester_begin = "09/01/2022"
semester_end = "12/31/2022"
lessons = calc_date(lessons, semester_begin, semester_end)

# lessons.to_excel("Lessons.xlsx", "List")
add_lessons(lessons)

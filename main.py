import pandas as pd

from pipelines.parse_group import parse_group
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher

# lessons = parse_timetable()
# lessons = parse_name(lessons)
lessons = pd.read_excel("parsed_lessons_table.xlsx", sheet_name=0)

lessons, teachers = parse_teacher(lessons)
lessons, groups = parse_group(lessons)
lessons, places = parse_place(lessons)
lessons, subjects = parse_subjects(lessons)
print(places)

import pandas as pd

from pipelines.completion import completion_groups
from pipelines.completion import completion_lecturers
from pipelines.completion import completion_rooms
from pipelines.id_instead_name import to_id
from pipelines.parse_group import parse_group
from pipelines.parse_place import parse_place
from pipelines.parse_subjects import parse_subjects
from pipelines.parse_teacher import parse_teacher

# lessons = parse_timetable()
# lessons = parse_name(lessons)
lessons = pd.read_excel("parsed_lessons_table.xlsx", sheet_name=0)
lessons = lessons.drop(columns=["id"])

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, subjects = parse_subjects(lessons)
lessons, teachers = parse_teacher(lessons)

completion_lecturers(teachers)
completion_rooms(places)
completion_groups(groups)

lessons = to_id(lessons)

with open("lessons.xlsx", "wb") as f:
    writer = pd.ExcelWriter(f, engine="xlsxwriter")
    lessons.to_excel(writer, index=False)
    writer.save()

from pipelines.parse_name import parse_name
from pipelines.parse_teacher import parse_teacher
from pipelines.parse_timetable import parse_timetable
import pandas as pd

# lessons = parse_timetable()
lessons = pd.read_excel("parsed_lessons_table.xlsx", sheet_name=0)
# lessons = parse_name(lessons)

lessons, teachers = parse_teacher(lessons)
print(lessons)
print(teachers)

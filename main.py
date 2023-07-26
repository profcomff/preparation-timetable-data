import passwords
import psycopg2
import datetime
from profcomff_parse_lib import *

headers = {"Authorization": f"{passwords.token}"}

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

# Временная мера, пока нет расписания летом.
conn = psycopg2.connect(
        host=passwords.host,
        database=passwords.database,
        user=passwords.user,
        password=passwords.password)

lessons = classical_parse_timetable(sources, conn)

# ---------------- Parsing ----------------
lessons = parse_name(lessons)
lessons, places, groups, teachers, subjects = parse_all(lessons)
lessons = manual_edit(lessons)
lessons = multiple_lessons(lessons)
lessons = flatten(lessons)
lessons.to_excel("lessons.xlsx", "1")
lessons = all_to_array(lessons)

# ---------------- Loading to server ----------------
completion(groups, places, teachers, headers, "test")
lessons = to_id(lessons, headers, "test")
be = datetime.datetime.now()
begin = be.strftime("%m/%d/%Y")
en = datetime.datetime.now() + datetime.timedelta(days=2)
end = en.strftime("%m/%d/%Y")

lessons = calc_date(lessons, begin, end)
delete_lessons(headers, begin, end, "test")
add_lessons(lessons, headers, "test")

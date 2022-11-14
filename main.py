from timetable import *


lessons = parse_timetable()
lessons = parse_name(lessons)

lessons, places = parse_place(lessons)
lessons, groups = parse_group(lessons)
lessons, teachers = parse_teacher(lessons)
lessons, subjects = parse_subjects(lessons)

# lessons = multiple_lessons(lessons)

lessons.to_excel("lessons.xlsx")

# completion_lecturers(teachers)
# completion_rooms(places)
# completion_groups(groups)
#
# lessons = to_id(lessons)
#
# semester_begin = "09/05/2022"
# semester_end = "09/18/2022"
# lessons = calc_date(lessons, semester_begin, semester_end)

# add_lessons(lessons)

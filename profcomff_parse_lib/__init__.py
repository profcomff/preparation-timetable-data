from .timetable.semester_parse_timetable import classical_parse_timetable
from .timetable.core.parse_name import parse_name
from .timetable.parse_all import parse_all
from .timetable.manual_edit import manual_edit
from .timetable.multiple_lessons import multiple_lessons
from .timetable.flatten import flatten
from .database.groups_to_array import all_to_array
from .database.completion import completion
from .database.id_instead_name import to_id
from .timetable.calc_date import calc_date
from .database.delete_lessons import delete_lessons
from .database.add_lessons import add_lessons
from .database.auto_updating import autoupdate

__all__ = ["classical_parse_timetable", "parse_name", "parse_all", "manual_edit", "multiple_lessons", "flatten",
           "all_to_array", "completion", "to_id", "calc_date", "delete_lessons", "add_lessons", "autoupdate"]

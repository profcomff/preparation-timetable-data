from database.add_lessons import add_lessons
from database.completion import completion_groups, completion_rooms, completion_lecturers
from database.id_instead_name import to_id
from database.delete_lessons import delete_lessons

__all__ = ["completion_groups", "completion_rooms", "completion_lecturers",
           "to_id", "add_lessons", "delete_lessons"]



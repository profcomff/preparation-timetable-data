from database.add_lessons import add_lessons
from database.completion import completion
from database.id_instead_name import to_id
from database.delete_lessons import delete_lessons
from database.groups_to_array import all_to_array

__all__ = ["completion",
           "to_id", "add_lessons", "delete_lessons", "all_to_array"]



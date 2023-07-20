from unittest import TestCase

import pandas as pd

from timetable.manual_edit import _delete_row


class Test(TestCase):
    def test__delete_row(self):
        data = pd.DataFrame({"1": [1, 1, 3, 4], "2": [3, 4, 2, 2]})

        new_data = _delete_row(data, {"1": 1})
        assert new_data["1"].to_list() == [3, 4]

        new_data = _delete_row(data, {"2": 2})
        assert new_data["1"].to_list() == [1, 1]

        new_data = _delete_row(data, {"1": 3, "2": 2})
        assert new_data["1"].to_list() == [1, 1, 4]
        assert new_data["2"].to_list() == [3, 4, 2]

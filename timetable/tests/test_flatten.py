from unittest import TestCase

import pandas as pd

from timetable.flatten import _to_list, flatten


class Test(TestCase):
    def test__to_list(self):
        assert _to_list("a") == ["a"]
        assert _to_list(["a"]) == ["a"]
        assert _to_list(None) == []
        assert _to_list(pd.NA) == []
        assert _to_list([["a"], "b"]) == ["a", "b"]
        assert _to_list(["a", None]) == ["a"]

    def test_flatten(self):
        data = pd.DataFrame(
            {'weekday': [0, 1, 2, 1],
             'group': [101, 102, 103, 104],
             'subject': [1, 3, 2, 4],
             'start': [0, 2, 1, 5],
             'teacher': [pd.NA, "1", ["2", "3"], "4"],
             'place': ["0", None, "3", ["3", "5"]]}
        )

        data = flatten(data)
        assert data["teacher"].to_list() == [[], ["1"], ["2", "3"], ["4"]]
        assert data["place"].to_list() == [["0"], [], ["3"], ["3", "5"]]


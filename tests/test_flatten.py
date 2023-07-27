from unittest import TestCase

import pandas as pd

from profcomff_parse_lib.timetable.flatten import flatten_to_list, flatten


class Test(TestCase):
    def test__to_list(self):
        assert flatten_to_list("a") == ["a"]
        assert flatten_to_list(["a"]) == ["a"]
        assert flatten_to_list(None) == []
        assert flatten_to_list(pd.NA) == []
        assert flatten_to_list([["a"], "b"]) == ["a", "b"]
        assert flatten_to_list(["a", None]) == ["a"]
        assert flatten_to_list([("a",), "b"]) == ["a", "b"]
        assert flatten_to_list(("a",)) == ["a"]

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


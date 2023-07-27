from unittest import TestCase
import pandas as pd

from profcomff_parse_lib.timetable import multiple_lessons


class Test(TestCase):
    def test_multiple_lessons(self):
        data = pd.DataFrame(
            {'weekday': [0, 2, 2, 1, 1],
             'group': [101, 103, 103, 107, 107],
             'subject': [1, 2, 2, 6, 6],
             'teacher': ['0', '2', '4', "5", "5"],
             'place': ['0', '3', '5', "7", "7"],
             "num": ["0", "1", "1", "4", "4"],
             "even": [True, True, True, True, False],
             "odd": [False, True, True, False, True]}
        )

        new_df = multiple_lessons(data)

        assert list(new_df['place']) == ['0', "7", ['3', '5']]
        assert list(new_df["teacher"]) == ["0", "5", ["2", "4"]]
        assert list(new_df['even']) == [True, True, True]
        assert list(new_df["odd"]) == [False, True, True]

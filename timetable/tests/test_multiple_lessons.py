from unittest import TestCase
import pandas as pd

from timetable.multiple_lessons import multiple_lessons


class Test(TestCase):
    def test_multiple_lessons(self):
        data = pd.DataFrame(
            {'weekday': [0, 1, 2, 1, 2],
             'group': [101, 102, 103, 104, 103],
             'subject': [1, 3, 2, 4, 2],
             'start': [0, 2, 1, 5, 1],
             'teacher': ['0', '1', '2', '3', '4'],
             'place': ['0', '1', '3', '3', '5']}
        )

        new_df = multiple_lessons(data)

        assert list(new_df['place']) == ['0', '1', '3', ['3', '5']]
        assert list(new_df["teacher"]) == ["0", "1", "3", ["2", "4"]]

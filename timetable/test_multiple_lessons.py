from unittest import TestCase
import pandas as pd

from fix_eng import _multiple_lessons

class Test(TestCase):
    def test__multiple_lessons (self):
        weekday = [0, 1, 2, 1, 2]
        group = [101, 102, 103, 104, 103]
        subject = [1, 3, 2, 4, 2]
        start = [0, 2, 1, 5, 1]
        teacher = ['0', '1', '2', '3', '4']
        place = ['0', '1', '3', '3', '5']

        data = pd.DataFrame(
            {'weekday': weekday,
            'group': group,
            'subject': subject,
            'start': start,
            'teacher': teacher,
            'place': place}
        )

        new_df = _multiple_lessons(data)
        result = list(new_df['place'])

        assert result == ['0', '1', '3', '3, 5']

from unittest import TestCase

import pandas as pd

from timetable import calc_date


class Test(TestCase):
    def test_calc_date(self):
        semester_begin = "09/01/2022"
        semester_end = "09/15/2022"
        df = pd.DataFrame(
            {
                'odd': [True, True, False],
                'even': [True, False, True],
                'num': [1, 2, 3],
                'weekday': [3, 4, 4],
                'start': ["9:00", "10:50", "13:30"],
                'end': ["10:35", "12:25", "15:05"],
                'subject': ['Кванты', 'Статы', 'Слупы']
            }
        )

        df_right = pd.DataFrame(
            {
                'start': ["2022-09-01T09:00:00Z", "2022-09-02T10:50:00Z", "2022-09-08T09:00:00Z",
                          "2022-09-09T13:30:00Z"],
                'end': ["2022-09-01T10:35:00Z", "2022-09-02T12:25:00Z", "2022-09-08T10:35:00Z", "2022-09-09T15:05:00Z"],
                'subject': ['Кванты', 'Статы', 'Кванты', 'Слупы']
            }
        )

        lessons = calc_date(df, semester_begin, semester_end)
        assert lessons["start"].to_list() == df_right["start"].to_list()
        assert lessons["end"].to_list() == df_right["end"].to_list()
        assert lessons["subject"].to_list() == df_right["subject"].to_list()

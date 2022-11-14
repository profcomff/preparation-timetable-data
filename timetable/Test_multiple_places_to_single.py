import unittest
import pandas as pd

from fix_eng import fix_eng

class Test_fix_func(unittest.TestCase):
    
    def test_ (self):
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

        new_df = multiple_lessons(data)
        place_col = list(new_df['place'])

        self.assertEqual(place_col, ['0', '1', '3', '3, 5'])

if __name__ == "__main__":
  unittest.main()

from unittest import TestCase
from timetable.pretty_subjects import _preprocessing


class Test(TestCase):
    def test__preprocessing(self):
        assert _preprocessing("   ЧЗХ") == "ЧЗХ"
        assert _preprocessing("ЧЗХ   ") == "ЧЗХ"
        assert _preprocessing("   ЧЗХ   ") == "ЧЗХ"

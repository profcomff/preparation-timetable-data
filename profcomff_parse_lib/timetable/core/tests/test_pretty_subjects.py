from unittest import TestCase

from profcomff_parse_lib.timetable.core.pretty_subjects import _preprocessing


class Test(TestCase):
    def test__preprocessing(self):
        assert _preprocessing("   ЧЗХ") == "ЧЗХ"
        assert _preprocessing("ЧЗХ   ") == "ЧЗХ"
        assert _preprocessing("   ЧЗХ   ") == "ЧЗХ"

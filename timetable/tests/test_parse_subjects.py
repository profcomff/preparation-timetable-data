from unittest import TestCase

from timetable.parse_subjects import _compare_groups, _parse_subjects


class Test(TestCase):
    def test__compare_groups(self):
        assert _compare_groups("307", "307")
        assert not _compare_groups("307", "308")
        assert _compare_groups("506ма", "506 Ма")
        assert _compare_groups("307", "307а")
        assert not _compare_groups("307м", "307ма")

    def test__parse_subjects(self):
        result = _parse_subjects("307", "307 - ЧЗХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("307", "308 - ЧЗХ")
        assert result is None

        result = _parse_subjects("308", "307,308,310 - ЧЗХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("308", "307,309,310 - ЧЗХ")
        assert result is None

        result = _parse_subjects("308", "307,308 - ЧЗХ,310,311 - ПНХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("310", "307,308 - ЧЗХ,310,311 - ПНХ")
        assert result == "ПНХ"

        result = _parse_subjects("309", "307,308 - ЧЗХ,310,311 - ПНХ")
        assert result is None

        result = _parse_subjects("309", "ЧЗХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("309", "15.10-18.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ")
        assert result == "15.10-18.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ"

        result = _parse_subjects("309", "1 поток без 307 группы - ЧЗХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("307", "1 поток без 307 группы - ЧЗХ")
        assert result is None

        result = _parse_subjects("309", "1 поток без 307 группы и астр. - ЧЗХ")
        assert result == "ЧЗХ"

        result = _parse_subjects("301", "1 поток без 307 группы и астр. - ЧЗХ")
        assert result is None

        result = _parse_subjects("103м", "103ма - Д/п, 103М - С/к, 140М - ФТД ")
        assert result == "С/к"


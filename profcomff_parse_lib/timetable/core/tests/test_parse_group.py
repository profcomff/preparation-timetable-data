from unittest import TestCase

from profcomff_parse_lib.timetable.core.parse_group import _parse_group


class Test(TestCase):
    def test__parse_group(self):
        result = _parse_group("113")
        assert result == [("113", "")]

        result = _parse_group("101 Специальность: астрономия")
        assert result == [("101", "Специальность: астрономия")]

        result = _parse_group("307-бандиты")
        assert result == [("307", "бандиты")]

        result = _parse_group("303, 304-бандиты")
        assert result == [("303", "бандиты"), ("304", "бандиты")]

        result = _parse_group("303, 304,305- бандиты")
        assert result == [("303", "бандиты"), ("304", "бандиты"), ("305", "бандиты")]

        result = _parse_group("303- бандиты/304-бандиты305-бандиты")
        assert result == [("303", "бандиты"), ("304", "бандиты"), ("305", "бандиты")]

        result = _parse_group("ОТДЕЛЕНИЕ ГЕОФИЗИКИ303 М- бандиты/304Мб-бандиты305-бандиты")
        assert result == [("303 М", "бандиты"), ("304Мб", "бандиты"), ("305", "бандиты")]

        result = _parse_group("303- бандиты304М-бандиты305 ма бандиты")
        assert result == [("303", "бандиты"), ("304М", "бандиты"), ("305 ма", "бандиты")]

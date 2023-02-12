from unittest import TestCase

from timetable import _parse_name


class Test(TestCase):
    def test__parse_name(self):
        result = _parse_name("Предмет <nobr>ЦФА</nobr> Гапочка А. М.")
        assert result == {"subject": "Предмет ", "teacher": " Гапочка А. М.", "place": "ЦФА"}

        result = _parse_name("Предмет <nobr>ЦФА</nobr>")
        assert result == {"subject": "Предмет ", "teacher": None, "place": "ЦФА"}

        result = _parse_name("Предмет Гапочка А. М.")
        assert result == {"subject": "Предмет", "teacher": "Гапочка А. М. ", "place": None}

        result = _parse_name("Предмет Гапочка А. М. Гапочка М. Г.")
        assert result == {"subject": "Предмет", "teacher": "Гапочка А. М. Гапочка М. Г. ", "place": None}

        result = _parse_name("Предмет")
        assert result == {"subject": "Предмет", "teacher": None, "place": None}

        result = _parse_name("118ма+118М - Предмет")
        assert result == {"subject": "118ма+118М - Предмет", "teacher": None, "place": None}

        result = _parse_name("15.10-18.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ")
        assert result == {"subject": "15.10-18.50 МЕЖФАКУЛЬТЕТСКИЕ КУРСЫ", "teacher": None, "place": None}

        result = _parse_name("429 - С/К по выбору доц. Водовозов В. Ю.")
        assert result == {"subject": "429 - С/К по выбору", "teacher": "доц. Водовозов В. Ю.", "place": None}


import pandas as pd
import requests

import timetable.timetable_parser as parser

# [[курс, поток, количество групп], ...]
sources = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 8],
    [5, 1, 13], [5, 2, 10],
    [6, 1, 10], [6, 2, 9]
]


def parse_timetable():
    """
    Получает данные с сайта расписания.
    """

    USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    HEADERS = {"User-Agent": USER_AGENT}

    results = pd.DataFrame()
    for index, source in enumerate(sources):
        for group in range(1, source[2] + 1):
            html = requests.get('http://ras.phys.msu.ru/table/{year}/{stream}/{group}.htm'
                                .format(year=source[0], stream=source[1], group=group), headers=HEADERS).text
            results = pd.concat([results, pd.DataFrame(parser.run(html))])
    # results["id"] = results.apply(lambda x: hashlib.md5("".join([i.__str__() for i in x]).encode()).hexdigest(), axis=1)

    return results

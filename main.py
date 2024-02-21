from profcomff_parse_lib import *
import pandas as pd
import logging
import requests as r

# [[курс, поток, количество групп], ...]
SOURCES = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 10],
    [5, 1, 13], [5, 2, 11],
    [6, 1, 11], [6, 2, 10]
]

USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

data = []
for ind, source in enumerate(SOURCES):
    for group in range(1, source[2]+1):
        url = f'http://ras.phys.msu.ru/table/{source[0]}/{source[1]}/{group}.htm'
        response = r.get(url, headers=HEADERS)
        logging.info("Page %s fetched with status %d", url, response.status_code)
        data.append({
            'url': url,
            'raw_html': response.text,
        })
timetables = pd.DataFrame(data)
results = pd.DataFrame()
for i, row in timetables.iterrows():
    results = pd.concat([results, parse_timetable(row["raw_html"])])

# ---------------- Parsing ----------------
lessons = parse_name(results)
lessons, places, groups, teachers, subjects = parse_all(lessons)
lessons = multiple_lessons(lessons)
lessons = flatten(lessons)
lessons = all_to_array(lessons)

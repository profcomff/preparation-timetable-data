# from profcomff_parse_lib import *
# from dotenv import load_dotenv
# import os
# import datetime
# import sqlalchemy as sa
# import pandas as pd
#
# load_dotenv()
# token = os.getenv("token")
# headers = {"Authorization": f"{token}"}
# host = os.getenv("host")
# database = os.getenv("database")
# user = os.getenv("user")
# password = os.getenv("password")
#
# schema = "STG_TIMETABLE"
# table = "raw_html"
# engine = sa.create_engine(f"postgresql://{database}:{user}@{host}/{password}")
# timetables = pd.read_sql_query(f'select * from "{schema}".{table}', engine)
#
# results = pd.DataFrame()
# for i, row in timetables.iterrows():
#     results = pd.concat([results, parse_timetable(row["raw_html"])])
#
# # ---------------- Parsing ----------------
# lessons = parse_name(results)
# lessons, places, groups, teachers, subjects = parse_all(lessons)
# lessons = manual_edit(lessons)
# lessons = multiple_lessons(lessons)
# lessons = flatten(lessons)
# lessons = all_to_array(lessons)
# a=1
# # ---------------- Loading to server ----------------
# # completion(groups, places, teachers, headers, "test")
# # lessons = to_id(lessons, headers, "test")
# # be = datetime.datetime.now()
# # begin = be.strftime("%m/%d/%Y")
# # en = datetime.datetime.now() + datetime.timedelta(days=2)
# # end = en.strftime("%m/%d/%Y")
# #
# # lessons = calc_date(lessons, begin, end, "07/24/2023")
# # delete_lessons(headers, begin, end, "test")
# # add_lessons(lessons, headers, "test")


from profcomff_parse_lib import *
import pandas as pd
import logging
import requests as r
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
token = os.getenv("token")
headers = {"Authorization": f"{token}"}

# [[курс, поток, количество групп], ...]
SOURCES = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 8],
    [5, 1, 13], [5, 2, 12],
    [6, 1, 13], [6, 2, 11]
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

completion(groups, places, teachers, headers, "test")
lessons = to_id(lessons, headers, "test")
be = datetime.datetime.now()
begin = be.strftime("%m/%d/%Y")
en = datetime.datetime.now() + datetime.timedelta(days=2)
end = en.strftime("%m/%d/%Y")

lessons = calc_date(lessons, begin, end, "07/24/2023")
delete_lessons(headers, begin, end, "test")
add_lessons(lessons, headers, "test")
a = 1

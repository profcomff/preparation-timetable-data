from profcomff_parse_lib import *
from dotenv import load_dotenv
import os
import datetime
import sqlalchemy as sa
import pandas as pd

load_dotenv()
token = os.getenv("token")
headers = {"Authorization": f"{token}"}
host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")

schema = "STG_TIMETABLE"
table = "raw_html"
engine = sa.create_engine(f"postgresql://{database}:{user}@{host}/{password}")
timetables = pd.read_sql_query(f'select * from "{schema}".{table}', engine)

results = pd.DataFrame()
for i, row in timetables.iterrows():
    results = pd.concat([results, parse_timetable(row["raw_html"])])

# ---------------- Parsing ----------------
lessons = parse_name(results)
lessons, places, groups, teachers, subjects = parse_all(lessons)
lessons = manual_edit(lessons)
lessons = multiple_lessons(lessons)
lessons = flatten(lessons)
lessons = all_to_array(lessons)
# ---------------- Loading to server ----------------
completion(groups, places, teachers, headers, "test")
lessons = to_id(lessons, headers, "test")
be = datetime.datetime.now()
begin = be.strftime("%m/%d/%Y")
en = datetime.datetime.now() + datetime.timedelta(days=2)
end = en.strftime("%m/%d/%Y")

lessons = calc_date(lessons, begin, end, "07/24/2023")
delete_lessons(headers, begin, end, "test")
add_lessons(lessons, headers, "test")

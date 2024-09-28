import time

import requests

from profcomff_parse_lib import *
import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
import os
from sqlalchemy.dialects import postgresql
import datetime

from profcomff_parse_lib.database.add_lessons import post_events

load_dotenv()
host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")

token = os.getenv("token")
headers = {"Authorization": f"{token}"}

schema = "public"
table = "raw_html"
engine = sa.create_engine(f"postgresql://{user}:{password}@{host}/{database}")
timetables = pd.read_sql_query(f'select * from "{schema}".{table}', engine)

results = pd.DataFrame()
for i, row in timetables.iterrows():
    results = pd.concat([results, parse_timetable(row["raw_html"])])

lessons = parse_name(results)
lessons, places, groups, teachers, subjects = parse_all(lessons)
lessons = manual_edit(lessons)
lessons = multiple_lessons(lessons)
lessons = flatten(lessons)
lessons = all_to_array(lessons)
completion(groups, places, teachers, headers, "prod")


lessons = to_id(lessons, headers, "prod")
conn = engine.connect()
conn.execute(sa.text(f"""
CREATE TABLE IF NOT EXISTS "{schema}".new(
	Id SERIAL PRIMARY key,
	subject varchar NOT NULL,
	odd bool NOT NULL,
	even bool NOT NULL,
	weekday INTEGER,
	num INTEGER,
	"start" varchar NOT NULL,
	"end" varchar NOT NULL,
	place INTEGER[],
	"group" INTEGER[],
	teacher INTEGER[],
	events_id INTEGER[]
);
"""))
conn.commit()
conn.execute(sa.text(f'DROP TABLE IF EXISTS "{schema}".old;'))
conn.execute(sa.text(f'DROP TABLE IF EXISTS "{schema}".diff;'))
conn.execute(sa.text(f'ALTER TABLE IF EXISTS "{schema}".new RENAME TO old;'))
conn.commit()
lessons.to_sql(name="new", con=engine, schema=schema, if_exists="replace", index=False,
               dtype={"group": postgresql.ARRAY(sa.types.Integer), "teacher": postgresql.ARRAY(sa.types.Integer),
                      "place": postgresql.ARRAY(sa.types.Integer)})
conn.execute(sa.text(f"""ALTER table "{schema}".new ADD id SERIAL PRIMARY key;"""))
conn.execute(sa.text(f"""ALTER table "{schema}".new ADD events_id INTEGER[];"""))
conn.commit()
conn.execute(sa.text(f"""UPDATE "{schema}".new set events_id =  ARRAY[]::integer[];"""))
conn.commit()
sql_query = f"""
create table "{schema}".diff as
select
	coalesce(l.subject, r.subject) as subject,
    coalesce(l.odd, r.odd) as odd,
    coalesce(l.even, r.even) as even,
    coalesce(l.weekday, r.weekday) as weekday,
    coalesce(l.num, r.num) as num,
    coalesce(l.start, r.start) as start,
    coalesce(l.end, r.end) as end,
    coalesce(l.place, r.place) as place,
    coalesce(l.group, r.group) as group,
    coalesce(l.teacher, r.teacher) as teacher,
    l.events_id,
    r.id,
    CASE
	    WHEN l.subject = r.subject THEN 'remember'
	    WHEN l.subject IS NULL THEN 'create'
	    WHEN r.subject IS NULL THEN 'delete'
END AS action
from "{schema}".old l
full outer join "{schema}".new r
    on l.subject = r.subject
    and  l.odd = r.odd
    and  l.even = r.even
    and  l.weekday  = r.weekday
    and  l.num  = r.num
    and  l.start = r.start
    and  l.end = r.end
    and  (l.place  <@ r.place  and l.place  @> r.place)
    and  (l.group  <@ r.group  and l.group  @> r.group)
    and  (l.teacher  <@ r.teacher  and l.teacher  @> r.teacher)
order by l.subject;
"""
conn.execute(sa.text(sql_query))
conn.commit()

lessons_for_deleting = pd.read_sql_query(f"""select events_id from "{schema}".diff where action='delete'""", engine)
lessons_for_creating = pd.read_sql_query(f"""select id, subject, "start", "end", "group", teacher, place, odd, even, weekday, num from "{schema}".diff where action='create'""", engine)

begin = datetime.datetime(year=2024, month=9, day=1)
end = datetime.datetime(year=2024, month=12, day=30)
begin = begin.strftime("%m/%d/%Y")
end = end.strftime("%m/%d/%Y")
for i, row in lessons_for_deleting.iterrows():
    for id in row["events_id"]:
        if check_date(id, "prod", begin):
            delete_lesson(headers, id, "prod")
lessons_new = calc_date(lessons_for_creating, begin, end, "09/01/2024")
a = 1
events = []
for i, event in lessons_new.iterrows():
    new_id = event["id"]
    events.append({
        "name": event['subject'],
        "room_id": event['place'],
        "group_id": event['group'],
        "lecturer_id": event['teacher'],
        "start_ts": event['start'],
        "end_ts": event['end']
    })
print(len(events))
batches = [events[i:i + 100] for i in range(0, len(events), 100)]
batches_error = []
for num, batch in enumerate(batches):
    resp = requests.post("https://api.profcomff.com/timetable/event/bulk", json=batch, headers=headers)
    if int(resp.status_code) == 502:
        batches_error.append(batch)
    print(f"{num+1}/{len(batches)} -- {resp}")
    time.sleep(0.1)

for num, batch in enumerate(batches_error):
    resp = requests.post("https://api.profcomff.com/timetable/event/bulk", json=batch, headers=headers)
    print(f"error-bacthes: {num+1}/{len(batches)} -- {resp}")
    time.sleep(0.1)


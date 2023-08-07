import requests
import os
import pandas as pd
import datetime
from retrying import retry
from requests.exceptions import RequestException
from .groups_to_array import separate
from profcomff_parse_lib.utilities import urls_api
from profcomff_parse_lib.timetable.semester_parse_timetable import classical_parse_timetable
from profcomff_parse_lib.timetable.core.parse_name import parse_name
from profcomff_parse_lib.timetable.parse_all import parse_all
from profcomff_parse_lib.timetable.manual_edit import manual_edit
from profcomff_parse_lib.timetable.multiple_lessons import multiple_lessons
from profcomff_parse_lib.timetable.flatten import flatten
from profcomff_parse_lib.database.groups_to_array import all_to_array
from profcomff_parse_lib.database.completion import completion
from profcomff_parse_lib.database.id_instead_name import to_id
from profcomff_parse_lib.timetable.calc_date import calc_date


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def post_event(url, headers, event):
    r = requests.post(url, json=event, headers=headers).json()
    return r["id"]


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def patch_event(url, headers, event):
    requests.patch(url, json=event, headers=headers).json()


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def delete_event(url, headers):
    requests.delete(url, headers=headers)


def get_old_table(engine, old_table_name):
    query = f'SELECT * FROM {old_table_name}'
    table = pd.read_sql_query(query, engine)
    column = [False]*len(table)
    table["correspond"] = column
    return separate(table)


def comparison(old, new):
    for i, part1 in enumerate(old):
        for j, el in enumerate(part1):
            old[i][j]["correspond"] = False

    for i, part1 in enumerate(new):
        for j, el in enumerate(part1):
            new[i][j]["correspond"] = False

    for i, part1 in enumerate(old):
        for j, el in enumerate(part1):
            for k, el1 in enumerate(new[i]):
                if (el["odd"] == el1["odd"] and el["even"] == el1["even"]
                        and el["rooms_id"] == el1["place"]
                        and el["groups_id"] == el1["group"]
                        and el["teachers_id"] == el1["teacher"]
                        and el["name"] == el1["subject"]):
                    old[i][j]["correspond"] = True
                    new[i][k]["correspond"] = True
                    break
    return old, new


def check_date(event_id, base, begin):
    r = requests.get(urls_api.get_url_event(urls_api.MODES_URL.get, base) + str(event_id))
    date_event = r.json()["start_ts"]
    date_event = date_event[:date_event.find("T")]
    date1 = datetime.datetime.strptime(begin, '%m/%d/%Y')
    date2 = datetime.datetime.strptime(date_event, '%Y-%m-%d')
    if date2 >= date1:
        return True
    else:
        return False


def update_long(old, new, begin, end, semester_start, headers, base):
    for_changing = []
    for_saving = []
    for part in old:
        for el in part:
            if not el["correspond"]:
                 for event_id in el["events_id"]:
                     if check_date(event_id, base, begin):
                        for_changing.append(event_id)

    for part in new:
        for el in part:
            if not el["correspond"]:
                new_el = el.drop(labels=["correspond"])
                for_saving.append(new_el)

    lessons = pd.DataFrame(for_saving)
    lessons.reset_index(drop=True, inplace=True)
    new = lessons
    lessons = calc_date(lessons, begin, end, semester_start)

    ar = [0] * new.shape[0]
    for ind in range(len(ar)):
        ar[ind] = []
    new["events_id"] = ar

    print(len(for_changing))
    print(lessons.shape[0])
    for Id in for_changing:
        url = urls_api.get_url_event(urls_api.MODES_URL.delete, base) + str(Id)
        delete_event(url, headers)
    for i, row in lessons.iterrows():
        request_body = {
            "name": row['subject'], "room_id": row['place'],
            "group_id": row['group'], "lecturer_id": row['teacher'],
            "start_ts": row['start'], "end_ts": row['end']
        }
        url = urls_api.get_url_event(urls_api.MODES_URL.post, base)
        new["events_id"][row["reference"]].append(post_event(url, headers, request_body))
    return new


def update_short(new, old, conn, table_name):
    old_new = []
    for part in old:
        for el in part:
            old_new.append(el)
    old = pd.DataFrame(old_new)

    cursor = conn.cursor()
    for i, row in old.iterrows():
        if not row["correspond"]:
            query = f'DELETE FROM {table_name} WHERE id = {row["id"]};'
            cursor.execute(query)
            conn.commit()

    new.rename(columns={'place': 'rooms_id', 'group': 'groups_id',
                        'teacher': 'teachers_id', 'subject': 'name',
                        'start': 'start_', 'end': 'end_'}, inplace=True)
    for i, row in new.iterrows():
        item = (row["name"], row["odd"], row["even"], row["weekday"], row["num"],
                row["start_"], row["end_"], row["rooms_id"],
                row["groups_id"], row["teachers_id"], row["events_id"])
        add_query = f"""
        INSERT INTO {table_name} (name, odd, even, weekday, num, start_, end_, 
        rooms_id, groups_id, teachers_id, events_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(add_query, item)
        conn.commit()


def autoupdate(sources, conn, engine, headers, table_name, semester_start, begin, end):
    new = classical_parse_timetable(sources, conn)
    new = parse_name(new)
    new, places, groups, teachers, subjects = parse_all(new)
    new = manual_edit(new)
    new = multiple_lessons(new)
    new = flatten(new)
    new = all_to_array(new)

    completion(groups, places, teachers, headers, "test")
    new = to_id(new, headers, "test")
    begin = begin.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")

    old = get_old_table(engine, table_name)
    old, new = comparison(old, separate(new))
    new = update_long(old, new, begin, end, semester_start, headers, "test")
    update_short(new, old, conn, table_name)

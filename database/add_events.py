import pandas as pd
import requests

from retrying import retry
from requests.exceptions import RequestException
import authorization

url_event = authorization.get_url() + '/timetable/event/'


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def add_lessons(lessons):
    for i, row in lessons.iterrows():
        name = row['subject']
        room_id = [int(row['place'])] if not pd.isna(row["place"]) else []
        group_id = int(row['group'])
        lecturer_id = row['teacher'] if isinstance(row["teacher"], list) else []
        start = row['start']
        end = row['end']
        event = {
            "name": name,
            "room_id": room_id,
            "group_id": group_id,
            "lecturer_id": lecturer_id,
            "start_ts": start,
            "end_ts": end
        }
        r = requests.post(url_event, json=event, headers=authorization.headers)
        print(r.json())

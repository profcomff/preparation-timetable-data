import json

import pandas as pd
import requests
from retrying import retry

from requests.exceptions import RequestException

# url = f"https://timetable.api.profcomff.com"
# beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})
# access_token = beaver.json().get("access_token")
#
# auth_data = json.loads(beaver.content)
#
# header = {"Authorization": f"Bearer {access_token}"}
# url_event = 'https://timetable.api.profcomff.com/timetable/event/'

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
access_token = beaver.json().get("access_token")

auth_data = json.loads(beaver.content)

header = {"Authorization": f"Bearer {access_token}"}
url_event = 'https://timetable.api.test.profcomff.com/timetable/event/'

@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def add_lessons(lessons):
    for i, row in lessons.iterrows():
        name = row['subject']
        room_id = row['place'] #row['place'])] if not pd.isna(row["place"]) else []
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
        r = requests.post(url_event, json=event, headers=header)
        print(r)

# for i in range(2000, 5000):
#     r = requests.get(url_event + str(i), headers=head)
#     print(r.json())
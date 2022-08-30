import json
import pandas as pd
import requests
import re
import numpy as np

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
auth_data = json.loads(beaver.content)

head = {"Authorization": f"Bearer {auth_data.get('access_token')}"}
url_event = 'https://timetable.api.test.profcomff.com/timetable/event/'


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
        requests.post('https://timetable.api.test.profcomff.com/timetable/event/', json=event, headers=head)




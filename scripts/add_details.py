import json

import pandas as pd
import requests

url = f"https://timetable.api.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})

access_token = beaver.json().get("access_token")
auth_data = json.loads(beaver.content)

header = {"Authorization": f"Bearer {access_token}"}

url_get = 'https://timetable.api.profcomff.com/timetable/lecturer/?limit=1000&offset=0&details=description'
url_patch = 'https://timetable.api.profcomff.com/timetable/lecturer/'


def add_full_name():
    prepods = pd.read_csv('prepods.csv', sep = ';')
    prepods_old = requests.get(url_get, headers=header).json()['items']
    for row in prepods_old:
        for i, row1 in prepods.iterrows():
            prep = row1['surname'].split()
            if len(prep) == 3:
                name = prep[0] + " " + prep[1][0] + ". " + prep[2][0] + "."
                if name == row['last_name'] + " " + row['first_name'] + " " + row['middle_name']:
                    row['first_name'] = prep[1]
                    row['middle_name'] = prep[2]
                    r = requests.patch(url_patch + str(row['id']),
                                   json=row, headers=header)
                    print(r)

add_full_name()
prepods_old = requests.get(url_get, headers=header).json()['items']

# for row in prepods_old:
#     if len(row['first_name']) > 2:
#         print(row)
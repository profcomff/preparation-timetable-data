import json

import pandas as pd
import requests

url = f"https://timetable.api.test.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})
auth_data = json.loads(beaver.content)

head = {"Authorization": f"Bearer {auth_data.get('access_token')}"}

def add_full_name():
    # st = {'last_name': 'Panin'}
    # print(requests.patch('https://timetable.api.test.profcomff.com/timetable/lecturer/1139', data=json.dumps(st), headers=head))
    # print(requests.get('https://timetable.api.test.profcomff.com/timetable/lecturer/1139', headers=head).json())
    prepods = pd.read_csv('prepods.csv', sep = ';')
    prepods_old = requests.get('https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0'
                               '&details=description', headers=head).json()['items']
    for row in prepods_old:
        for i, row1 in prepods.iterrows():
            prep = row1['surname'].split()
            if len(prep) == 3:
                name = prep[0] + " " + prep[1][0] + ". " + prep[2][0] + "."
                if name == row['last_name'] + " " + row['first_name'] + " " + row['middle_name']:
                    row['first_name'] = prep[1]
                    row['middle_name'] = prep[2]
                    requests.patch('https://timetable.api.test.profcomff.com/timetable/lecturer/' + str(row['id']),
                                   json=row, headers=head)

add_full_name()
prepods_old = requests.get('https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0'
                               '&details=description', headers=head).json()['items']

for row in prepods_old:
    if len(row['first_name']) > 2:
        print(row)
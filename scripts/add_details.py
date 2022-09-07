import json

import pandas as pd
import requests
import authorization

url_get = authorization.get_url() + '/timetable/lecturer/?limit=1000&offset=0&details=description'
url_patch = authorization.get_url() + '/timetable/lecturer/'


def add_full_name():
    prepods = pd.read_csv('prepods.csv', sep=';')
    prepods_old = requests.get(url_get, headers=authorization.headers).json()['items']
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
prepods_old = requests.get(url_get, headers=authorization.headers).json()['items']

import pandas as pd
import requests

import authorization as au
import password

headers = {}
# au.authorization(password.login, password.password)
url = au.get_url()
beaver = requests.post(f"{url}/token", {"username": password.login, "password": password.password})
access_token = beaver.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}


def fix_eng(lessons):
    url_group = au.get_url_group(au.MODES_URL.get)
    r = requests.get(url_group, headers=headers)
    groups = r.json()['items']
    groups = pd.DataFrame(groups)

    new_lessons = []

    n_lessons = []
    for i, row in lessons.iterrows():
        row['place'] = [int(row['place'])] if not pd.isna(row["place"]) else []
        if not isinstance(row["teacher"], list):
            row['teacher'] = []
        n_lessons.append(row)

    lessons = pd.DataFrame(n_lessons)
    lessons.to_excel("test.xlsx", "List")

    for i, group in groups.iterrows():
        for number_day in range(7):
            table = []

            for k, row in lessons.iterrows():
                if row['group'] == group[0] and row['weekday'] == number_day:
                    table.append(row)
            table = pd.DataFrame(table)

            row1 = pd.DataFrame()
            array = []
            flag = False

            for k, row in table.iterrows():
                if "странный язык" in row['subject']:
                    row1 = row
                    flag = True
                    array.append(k)
                    break

            for k, row in table.iterrows():
                if row['teacher']:
                    if "странный язык" in row['subject'] and row['teacher'][0] != row1['teacher'][0]:
                        array.append(k)
                        row1['teacher'].append(row['teacher'][0])
                        row1['place'].append(row['place'][0])

            table.drop(labels=array, axis=0, inplace=True)
            if flag:
                new_lessons.append(row1)

            for k, row in table.iterrows():
                new_lessons.append(row)

    new_lessons = pd.DataFrame(new_lessons)
    return new_lessons

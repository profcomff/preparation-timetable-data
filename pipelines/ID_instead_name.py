import numpy as np
import pandas as pd
import requests
import json

url = f"https://timetable.api.test.profcomff.com"

# Авторизация
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})

# Парсинг ответа
auth_data = json.loads(beaver.content)


def get_teachers():
    a = requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0',
                     headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    b = json.dumps(a.json())
    jteachers = json.loads(b)
    teachers = pd.DataFrame(jteachers['items'])
    #print(teachers)
    return teachers


def to_id(lessons):
    teachers = get_teachers()
    print(lessons)
    print(teachers)
    for i in range(len(lessons)):
        for j in range(len(teachers)):
            #if isinstance(lessons[i, 'teacher'], list):
                name = str(teachers.loc[j, 'last_name']) + " " + str((teachers.loc[j, 'first_name'])[0]) + "." + " " + str(teachers.loc[j, 'middle_name'][0]) + ".";
                print(str(teachers.loc[j, 'last_name']))
                if str(lessons.loc[i, 'teacher']).__contains__(name):
                    lessons.loc[i, 'teacher'] = teachers.loc[j, 'id']
                    break
    return lessons


# a = to_id()
#
# get_teachers()

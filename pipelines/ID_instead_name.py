import numpy as np
import pandas as pd
import requests
import json

url=f"https://timetable.api.test.profcomff.com"

# Авторизация
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})

# Парсинг ответа
auth_data=json.loads(beaver.content)

def get_teachers():
    a = requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    b = json.dumps(a.json())
    jteachers = json.loads(b)
    teachers = pd.DataFrame(jteachers['items'])
    print(teachers)
    return teachers

def to_id():
    teachers = get_teachers()
    b = pd.read_excel('parsed_lessons_table (3).xlsx')
    for i in range(len(b)):
        for j in range(len(a)):
            if(str(b.loc[i, 'teacher']).__contains__(str(a.loc[j, 'Фамилия И. О.']))):
                b.loc[i, 'teacher'] = str(a.loc[j, 'id'])
    return b

a = to_id()

get_teachers()
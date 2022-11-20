import urllib
import os
from urllib.request import urlopen

import pandas as pd
import requests
from utilities import urls_api as au
import password
from requests.exceptions import RequestException
from retrying import retry

url = au.get_url()
beaver = requests.post(f"{url}/token", {"username": password.login, "password": password.password})
access_token = beaver.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

url_get_lecturer = url + '/timetable/lecturer/?limit=1000&offset=0&details=description'
url_patch_lecturer = url + '/timetable/lecturer/'

url_get_room = url + '/timetable/room/?limit=1000&offset=0'
url_patch_room = url + '/timetable/room/'


def add_full_name():
    prepods = pd.read_excel('Дубина. Рабочая таблица (2).xlsx', sheet_name= 'Lecturers')
    prepods_old = requests.get(url_get_lecturer, headers=headers).json()['items']
    for row in prepods_old:
        for i, row1 in prepods.iterrows():
            if row['last_name'] == row1['last_name'] and row['first_name'][0] == row1['first_name'][0] and row['last_name'][0] == row1['last_name'][0]:
                row['first_name'] = row1['first_name']
                row['middle_name'] = row1['middle_name']
                row['last_name'] = row1['last_name']
                r = requests.patch(url_patch_lecturer + str(row['id']), json=row, headers=headers)
                print(r)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def Apploading(url_post, files):
    res = requests.post(url=url_post, files=files)
    print('Apploading: ', res)
    return res.json()['id']

@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def image(link):
    img = urllib.request.urlopen(link).read()
    out = open("img.png", "wb")
    out.write(img)
    out.close()
    with open('img.png', 'rb') as f:
        data = f.read()
    return data


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def approving(lecturer_id, photo_id):
    res = requests.post(
        url=f'{url}/timetable/lecturer/{lecturer_id}/photo/{photo_id}/review/?action=Approved',
        headers=headers)
    print("Approving: ", res)


@retry(retry_on_exception=lambda e: isinstance(e, RequestException), wait_exponential_multiplier=1000,
       wait_exponential_max=30000, stop_max_attempt_number=30)
def updating(lecturer_id, photo_id):
    res = requests.patch(url=f'{url}/timetable/lecturer/{lecturer_id}', json={"avatar_id": photo_id},
                         headers=headers)
    print(photo_id, "Updating: ", res)


def add_photos():
    prepods = pd.read_excel('Дубина. Рабочая таблица (2).xlsx', sheet_name='Lecturers')
    prepods_old = requests.get(url_get_lecturer, headers=headers).json()['items']
    for row in prepods_old:
        for i, row1 in prepods.iterrows():
            if row['last_name'] == row1['last_name'] and row['first_name'][0] == row1['first_name'][0] and row['last_name'][0] == row1['last_name'][0]:
                if not pd.isna(row1['photo_link']):
                    lecturer_id = row['id']
                    data = image(row1['photo_link'])

                    if os.stat('img.png').st_size >= 3000000:
                        break

                    url_post = f'{url}/timetable/lecturer/{lecturer_id}/photo'
                    files = {"photo": data}
                    photo_id = Apploading(url_post, files)

                    approving(lecturer_id, photo_id)
                    updating(lecturer_id, photo_id)
                    break


def add_direction():
    rooms = pd.read_excel("Дубина. Рабочая таблица (2).xlsx", sheet_name="Rooms")
    rooms_old = requests.get(url_get_room, headers=headers).json()['items']
    for row in rooms_old:
        for i, row1 in rooms.iterrows():
            if row['name'] == row1['room']:
                # row['direction'] = str(row1['direction'])
                new_room = {}
                if row1['direction'] == 'south':
                    new_room = {"direction": "South"}
                if row1['direction'] == 'north':
                    new_room = {"direction": "North"}
                r = requests.patch(url_patch_room + str(row['id']), json=new_room, headers=headers)
                print(r)
                break


def prepods_comment():
    prepods = pd.read_excel('Дубина. Рабочая таблица (2).xlsx', sheet_name='Lecturers')
    prepods_old = requests.get(url_get_lecturer, headers=headers).json()['items']
    for row in prepods_old:
        for i, row1 in prepods.iterrows():
            if row['last_name'] == row1['last_name'] and row['first_name'][0] == row1['first_name'][0] and row['last_name'][0] == row1['last_name'][0]:
                if not pd.isna(row1['faculty']):
                    text = row1['faculty']
                    if not pd.isna(row1['department']):
                        if row1['department'] != row1['faculty']:
                            text += ", " + row1['department']
                    res = requests.patch(url=url_patch_lecturer + str(row['id']), json={"description": text}, headers=headers)
                    print(res.json())


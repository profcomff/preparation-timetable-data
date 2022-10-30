import requests
import json

import authorization as au
import password

headers = {}
# au.authorization(password.login, password.password)
url = au.get_url()
beaver = requests.post(f"{url}/token", {"username": password.login, "password": password.password})
access_token = beaver.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

def delete_rooms():
    rooms = requests.get(au.get_url_room(au.MODES_URL.get), headers=headers).json()

    for i in range(len(rooms['items'])):
        r = requests.delete(au.get_url_room(au.MODES_URL.delete) + str(rooms['items'][i]['id']), headers=headers)
        print(r)


def delete_groups():

    groups = requests.get(au.get_url_group(au.MODES_URL.get), headers=au.headers).json()
    for i in range(len(groups['items'])):
        r = requests.delete(au.get_url_group(au.MODES_URL.delete) + str(groups['items'][i]['id']), headers=headers)
        print(r)


def delete_lecturers():
    lecturers = requests.get(au.get_url_lecturer(au.MODES_URL.get), headers=au.headers).json()
    for i in range(len(lecturers['items'])):
        r = requests.delete(au.get_url_lecturer(au.MODES_URL.delete)+ str(lecturers['items'][i]['id']), headers=headers)
        print(r)


def delete_events():
    for i in range(9000, 9050):
        r = requests.delete(au.get_url_event(au.MODES_URL.delete) + str(i), headers=headers)
        print(r)


delete_events()
delete_lecturers()
print(au.headers)
# print(str(au.get_url_group(au.MODES_URL.delete) + "2"))
# r = requests.delete(au.get_url_group(au.MODES_URL.delete) + "2", headers=au.headers)
# print(r)
delete_groups()
delete_rooms()

import requests
import json

import authorization

url_get_lecturer = authorization.get_url() + '/timetable/lecturer/?limit=1000&offset=0&details=description'
url_delete_lecturer = authorization.get_url() + '/timetable/lecturer/'

url_get_room = authorization.get_url() + '/timetable/room/?limit=1000&offset=0'
url_delete_room = authorization.get_url() + '/timetable/room/'

url_get_group = authorization.get_url() + '/timetable/group/?limit=1000&offset=0'
url_delete_group = authorization.get_url() + '/timetable/group/'


def delete_rooms():
    print("___________________________________________________")
    rooms = requests.get(url_get_room, headers=authorization.headers).json()

    for i in range(len(rooms['items'])):
        r = requests.delete(url_delete_room + str(rooms['items'][i]['id']), headers=authorization.headers)
        print(r)


def delete_groups():
    print("___________________________________________________")

    groups = requests.get(url_get_group, headers=authorization.headers).json()
    for i in range(len(groups['items'])):
        r = requests.delete(url_delete_group + str(groups['items'][i]['id']), headers=authorization.headers)
        print(r)


def delete_lecturers():
    print("___________________________________________________")
    url1 = 'https://timetable.api.test.profcomff.com/timetable/lecturer/'
    lecturers = requests.get(url_get_lecturer, headers=authorization.headers).json()
    for i in range(len(lecturers['items'])):
        r = requests.delete(url_delete_lecturer + str(lecturers['items'][i]['id']), headers=authorization.headers)
        print(r)


def delete_events():
    print("___________________________________________________")
    url_event = authorization.get_url() + '/timetable/event/'
    for i in range(69000, 80000):
        r = requests.delete(url_event + str(i), headers=authorization.headers)
        print(r)


# delete_events()
# delete_lecturers()
delete_groups()
# delete_rooms()

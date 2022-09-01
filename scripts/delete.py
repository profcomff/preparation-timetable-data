import requests
import json

url = f"https://timetable.api.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})
access_token = beaver.json().get("access_token")
auth_data = json.loads(beaver.content)
head = {"Authorization": f"Bearer {access_token}"}


def delete_rooms():
    url1 = 'https://timetable.api.profcomff.com/timetable/room/'
    rooms = requests.get(f'https://timetable.api.profcomff.com/timetable/room/?limit=1000&offset=0',
                         headers=head).json()
    for i in range(len(rooms['items'])):
        r = requests.delete(url1 + str(rooms['items'][i]['id']),
                            headers=head)
        print(r)


def delete_groups():
    url1 = 'https://timetable.api.test.profcomff.com/timetable/group/'
    groups = requests.get(f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0',
                          headers=head).json()
    for i in range(len(groups['items'])):
        r = requests.delete(url1 + str(groups['items'][i]['id']),
                            headers=head)
        print(r)


def delete_lecturers():
    url1 = 'https://timetable.api.test.profcomff.com/timetable/lecturer/'
    lecturers = requests.get(f'https://timetable.api.profcomff.com/timetable/lecturer/?limit=1000&offset=0',
                             headers=head).json()
    for i in range(len(lecturers['items'])):
        r = requests.delete(url1 + str(lecturers['items'][i]['id']),
                            headers=head)
        print(r)


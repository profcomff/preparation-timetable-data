import requests
import json

url = f"https://timetable.api.profcomff.com"
beaver = requests.post(f"{url}/token", {"username": "timetable_fill", "password": "J2Jmc9mgn31jeSGa"})
access_token = beaver.json().get("access_token")
auth_data = json.loads(beaver.content)
head = {"Authorization": f"Bearer {access_token}"}


def delete_rooms():
    print("___________________________________________________")
    url1 = 'https://timetable.api.profcomff.com/timetable/room/'
    rooms = requests.get(f'https://timetable.api.profcomff.com/timetable/room/?limit=1000&offset=0',
                         headers=head).json()

    for i in range(len(rooms['items'])):
        r = requests.delete(url1 + str(rooms['items'][i]['id']),
                            headers=head)
        print(r)


def delete_groups():
    print("___________________________________________________")
    url1 = 'https://timetable.api.test.profcomff.com/timetable/group/'

    groups = requests.get(f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0',
                          headers=head).json()
    for i in range(len(groups['items'])):
        r = requests.delete(url1 + str(groups['items'][i]['id']),
                            headers=head)
        print(r)

def delete_lecturers():
    print("___________________________________________________")
    url1 = 'https://timetable.api.test.profcomff.com/timetable/lecturer/'
    lecturers = requests.get(f'https://timetable.api.profcomff.com/timetable/lecturer/?limit=1000&offset=0',
                             headers=head).json()
    for i in range(len(lecturers['items'])):
        r = requests.delete(url1 + str(lecturers['items'][i]['id']),
                            headers=head)
        print(r)

# url1 = 'https://timetable.api.test.profcomff.com/timetable/group/'
# groups = requests.get(f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0',
#                           headers=head).json()
# print(groups)


def delete_events():
    print("___________________________________________________")
    url_event = 'https://timetable.api.profcomff.com/timetable/event/'
    for i in range(69000, 80000):
        r = requests.delete(url_event + str(i), headers=head)
        print(r)


# delete_events()
# delete_lecturers()
delete_groups()
# delete_rooms()

groups = requests.get(f'https://timetable.api.profcomff.com/timetable/group/?limit=1000&offset=0',
                          headers=head).json()
print(groups)
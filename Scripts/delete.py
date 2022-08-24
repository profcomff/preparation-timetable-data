import requests
import json

url=f"https://timetable.api.test.profcomff.com"

# Авторизация
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})

# Парсинг ответа
auth_data=json.loads(beaver.content)

def delete_rooms():
    url1 = 'https://timetable.api.test.profcomff.com/timetable/room/'
    rooms = requests.get(f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json()
    for i in range(len(rooms['items'])):
        r = requests.delete(url1 + str(rooms['items'][i]['id']), headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
        print(r)

def delete_groups():
    url1 = 'https://timetable.api.test.profcomff.com/timetable/group/'
    groups = requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json()
    for i in range(len(groups['items'])):
        r = requests.delete(url1 + str(groups['items'][i]['id']), headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
        print(r)

def delete_lecturers():
    url1 = 'https://timetable.api.test.profcomff.com/timetable/lecturer/'
    lecturers = requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0',
                          headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json()
    for i in range(len(lecturers['items'])):
        r = requests.delete(url1 + str(lecturers['items'][i]['id']),
                            headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
        print(r)

delete_rooms()
delete_groups()
delete_lecturers()
print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())
print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())
print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())
import requests
import json

url=f"https://timetable.api.test.profcomff.com"

# Авторизация
beaver = requests.post(f"{url}/token", {"username": "admin", "password": "42"})

# Парсинг ответа
auth_data=json.loads(beaver.content)

# r = requests.delete(f'https://timetable.api.test.profcomff.com/timetable/lecturer/6', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
# print(r)

def completion_lecturers(new_lecturers):
    a = requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    b = json.dumps(a.json())
    old_lecturers = json.loads(b)
    n = len(new_lecturers)
    m = len(old_lecturers['items'])
    b = False
    for i in range(n):
        for j in range(m):
            b1 = (new_lecturers[i]).split()[0] == old_lecturers['items'][j]['last_name']
            b2 = (new_lecturers[i].split()[1])[0] == (old_lecturers['items'][j]['first_name'])[0]
            b3 = (new_lecturers[i].split()[2])[0] == (old_lecturers['items'][j]['middle_name'])[0]
            b = b1 and b2 and b3
            if(b):
                break

        if(b == False):
            last_name = new_lecturers[i].split()[0]
            first_name = new_lecturers[i].split()[1]
            middle_name = new_lecturers[i].split()[2]
            data = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name}
            requests.post(f'https://timetable.api.test.profcomff.com/timetable/lecturer/', json=data, headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})

def completion_rooms(new_rooms):
    a = requests.get(f'https://timetable.api.test.profcomff.com/timetable/room/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    b = json.dumps(a.json())
    old_rooms = json.loads(b)
    n = len(new_rooms)
    m = len(old_rooms['items'])
    b = False
    for i in range(n):
        for j in range(m):
            b = new_rooms[i] == old_rooms['items'][j]['name']
            if(b):
                break

        if(b == False):
            name = new_rooms[i]
            data = {'name': name, 'direction': None}
            requests.post(f'https://timetable.api.test.profcomff.com/timetable/room/', json=data, headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})

def completion_groups(new_groups):
    a = requests.get(f'https://timetable.api.test.profcomff.com/timetable/group/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})
    b = json.dumps(a.json())
    old_groups = json.loads(b)
    n = len(new_groups)
    m = len(old_groups['items'])
    b = False
    for i in range(n):
        for j in range(m):
            b1 = new_groups[i][0] == old_groups['items'][j]['number']
            b2 = new_groups[i][1] == old_groups['items'][j]['name']
            b = b1 and b2
            if (b):
                break

        if (b == False):
            number = new_groups[i][0]
            name = new_groups[i][1]
            data = {'name': name, 'number': number}
            requests.post(f'https://timetable.api.test.profcomff.com/timetable/gruop/', json=data,
                          headers={"Authorization": f"Bearer {auth_data.get('access_token')}"})


new_lecturers = ["last_name fsdg msgdgv", "Иванов И. И."]
completion_lecturers(new_lecturers)
#data = {'first_name': 'first_name', 'middle_name': 'm.', 'last_name': 'l.'}
print(requests.get(f'https://timetable.api.test.profcomff.com/timetable/lecturer/?limit=1000&offset=0', headers={"Authorization": f"Bearer {auth_data.get('access_token')}"}).json())

# data = []
# a = 'foo'
# data.append(a) # добавление в список 'data'
# b = {'bar': ['baz', None, 1.0, 2], 'key': 'value', 10: 'ten'}
# data.append(b)
# c = [3, 4, 5, 6]
# data.append(c)
#
# # Преобразование объекта Python
# # в строку формата JSON
# json_data = json.dumps(data, indent=4)
# print(json_data)


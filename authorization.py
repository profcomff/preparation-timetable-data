import enum
import requests

headers = {}

MODES = enum.Enum("Modes", "test prod")
mode = MODES.test

# mode = "test"

TEST_URL = "https://timetable.api.test.profcomff.com"
PROD_URL = "https://timetable.api.profcomff.com"


def get_url():
    if mode == MODES.prod:
        return PROD_URL
    else:
        return TEST_URL


def authorization(login, passoword):
    url = get_url()
    beaver = requests.post(f"{url}/token", {"username": login, "password": passoword})
    access_token = beaver.json().get("access_token")
    authorization.headers = {"Authorization": f"Bearer {access_token}"}





import enum

MODES = enum.Enum("Modes", "test prod")
mode = MODES.test

MODES_URL = enum.Enum("Modes", "get delete post patch")


def get_url_room(mode_):
    if mode_ == MODES_URL.get:
        return get_url() + "/timetable/room/?limit=1000&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url() + '/timetable/room/'
    if mode_ == MODES_URL.post:
        print("yes")
        return get_url() + '/timetable/room/'
    if mode_ == MODES_URL.patch:
        return get_url() + '/timetable/room/'


def get_url_group(mode_):
    if mode_ == MODES_URL.get:
        return get_url() + "/timetable/group/?limit=1000&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url() + '/timetable/group/'
    if mode_ == MODES_URL.post:
        return get_url() + '/timetable/group/'
    if mode_ == MODES_URL.patch:
        return get_url() + '/timetable/group/'


def get_url_lecturer(mode_):
    if mode_ == MODES_URL.get:
        return get_url() + "/timetable/lecturer/?limit=1000&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url() + '/timetable/lecturer/'
    if mode_ == MODES_URL.post:
        return get_url() + '/timetable/lecturer/'
    if mode_ == MODES_URL.patch:
        return get_url() + '/timetable/lecturer/'


def get_url_event(mode_):
    if mode_ == MODES_URL.get:
        return get_url() + "/timetable/event/"
    if mode_ == MODES_URL.delete:
        return get_url() + '/timetable/event/'
    if mode_ == MODES_URL.post:
        return get_url() + '/timetable/event/'
    if mode_ == MODES_URL.patch:
        return get_url() + '/timetable/event/'


TEST_URL = "https://timetable.api.test.profcomff.com"
PROD_URL = "https://timetable.api.profcomff.com"


def get_url():
    if mode == MODES.prod:
        return PROD_URL
    else:
        return TEST_URL

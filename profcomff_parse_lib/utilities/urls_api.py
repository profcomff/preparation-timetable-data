import enum

# MODES = enum.Enum("Modes", "test prod")
# mode = MODES.test


MODES_URL = enum.Enum("Modes", "get delete post patch")


def get_url_room(mode_, base):
    if mode_ == MODES_URL.get:
        return get_url(base) + "/timetable/room/?limit=0&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url(base) + '/timetable/room/'
    if mode_ == MODES_URL.post:
        return get_url(base) + '/timetable/room/'
    if mode_ == MODES_URL.patch:
        return get_url(base) + '/timetable/room/'


def get_url_group(mode_, base):
    if mode_ == MODES_URL.get:
        return get_url(base) + "/timetable/group/?limit=0&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url(base) + '/timetable/group/'
    if mode_ == MODES_URL.post:
        return get_url(base) + '/timetable/group/'
    if mode_ == MODES_URL.patch:
        return get_url(base) + '/timetable/group/'


def get_url_lecturer(mode_, base):
    if mode_ == MODES_URL.get:
        return get_url(base) + "/timetable/lecturer/?limit=0&offset=0"
    if mode_ == MODES_URL.delete:
        return get_url(base) + '/timetable/lecturer/'
    if mode_ == MODES_URL.post:
        return get_url(base) + '/timetable/lecturer/'
    if mode_ == MODES_URL.patch:
        return get_url(base) + '/timetable/lecturer/'


def get_url_event(mode_, base):
    if mode_ == MODES_URL.get:
        return get_url(base) + "/timetable/event/"
    if mode_ == MODES_URL.delete:
        return get_url(base) + '/timetable/event/'
    if mode_ == MODES_URL.post:
        return get_url(base) + '/timetable/event/'
    if mode_ == MODES_URL.patch:
        return get_url(base) + '/timetable/event/'


TEST_URL = "https://api.test.profcomff.com"
PROD_URL = "https://api.profcomff.com"

def get_url(base):
    if base == "prod":
        return PROD_URL
    if base == "test":
        return TEST_URL

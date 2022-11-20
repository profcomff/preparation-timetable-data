import argparse


def get_parser():
    """Return the necessary parser."""
    parser = argparse.ArgumentParser(description="The program for loading the timetable into the database")
    parser.add_argument("login", help="login")
    parser.add_argument("password", help="password")
    parser.add_argument("-db", dest="database", default="test", help="database (default: test)",
                        const="test", nargs="?", choices=["test", "prod"])
    parser.add_argument("--debug_parse", action="store_true",
                        help="if true save data to excel and don't upload it to server (default: false)")
    parser.add_argument("-begin", default="09/05/2022",
                        help="beginning of semester (default: 09/05/2022) "
                             "(WARNING: value must be in same format as default argument)")
    parser.add_argument("-end", default="09/18/2022",
                        help="end of semester (default: 09/18/2022) "
                             "(WARNING: value must be in same format as default argument)")
    parser.add_argument("-log", dest="log_level", default="info", help="level of logging on console (default: info)",
                        const="info", nargs="?", choices=["info", "debug"])
    return parser

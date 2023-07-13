import argparse


def get_parser():
    """Return the necessary parser."""
    parser = argparse.ArgumentParser(description="The program for loading the timetable into the database")
    parser.add_argument("login", help="login")
    parser.add_argument("password", help="password")
    parser.add_argument("-db", dest="database", default="test", help="database (default: test)",
                        const="test", nargs="?", choices=["test", "prod"])
    parser.add_argument("--debug", action="store_true",
                        help="if true sets debug level of logging for console (default: false)")
    parser.add_argument("-begin", default="09/05/2022",
                        help="beginning of semester (default: 09/05/2022) "
                             "(WARNING: value must be in same format as default argument)")
    parser.add_argument("-end", default="09/18/2022",
                        help="end of semester (default: 09/18/2022) "
                             "(WARNING: value must be in same format as default argument)")
    return parser

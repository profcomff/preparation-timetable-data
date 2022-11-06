import argparse


def get_parser():
    """Return the necessary parser."""
    parser = argparse.ArgumentParser(description="The program for loading the timetable into the database")
    parser.add_argument("login", help="login")
    parser.add_argument("password", help="password")
    parser.add_argument("-db", dest="database", default="test", help="database (default: test)",
                        const="test", nargs="?", choices=["test", "prod"])
    parser.add_argument("--debug", action="store_true",
                        help="if true save data to excel and don't upload it to server (default: false)")
    parser.add_argument("-begin", default="09/05/2022",
                        help="beginning of semester (default: 09/05/2022) "
                             "(WARNING: value must be in same format as default argument)")
    parser.add_argument("-end", default="09/18/2022",
                        help="end of semester (default: 09/18/2022) "
                             "(WARNING: value must be in same format as default argument)")
    return parser


def get_url_engine(args):
    """
    Return the url for the alchemy engine.
    >>> get_url_engine(get_parser().parse_args("login password -db=test".split()))
    'postgresql+psycopg2://login:password@db.profcomff.com:25432/test'

    :param args: Args from parser from 'get_parser' (see above).
    """
    return f"postgresql+psycopg2://{args.login}:{args.password}@db.profcomff.com:25432/{args.database}"


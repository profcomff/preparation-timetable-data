import psycopg2
from dotenv import load_dotenv
import os
from profcomff_parse_lib import autoupdate

load_dotenv()
sources = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 8],
    [5, 1, 13], [5, 2, 11],
    [6, 1, 11], [6, 2, 10]
]
conn = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"))
autoupdate(sources, conn, "07/24/2023")

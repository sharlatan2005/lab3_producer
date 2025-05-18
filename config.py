from os import getenv
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = getenv('SQLITE_PATH')
SQLITE_TABLE_NAME = getenv('SQLITE_TABLE_NAME')

GRPC_PORT = getenv('GRPC_PORT')
import os

PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(PACKAGE_DIR, 'data')
CRYPT_FILE_PATH = os.path.join(DATA_DIR, 'cardbase_crypt.json')
LIBRARY_FILE_PATH = os.path.join(DATA_DIR, 'cardbase_lib.json')

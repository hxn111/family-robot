# Better to use an env file but this will do for now
import os
BASE_DIR = '/home/pi/'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
PICS_DIR = os.path.join(ASSETS_DIR, 'pics')

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(PICS_DIR, exist_ok=True)
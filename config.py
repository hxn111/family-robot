import os
import redis

# some of these might be better set in an ignored .env file..
# but this will do for now
BASE_DIR = '/home/pi/'
GIT_DIR = '/home/pi/family-robot'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
PICS_DIR = os.path.join(ASSETS_DIR, 'pics')
VIDS_DIR = os.path.join(ASSETS_DIR, 'videos')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
SYS_AUDIO_DIR = os.path.join(GIT_DIR, 'sound')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(PICS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDS_DIR, exist_ok=True)

# Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
R_KEY_LAST_FRAME = 'last_frame'

# mic
MIC_DEVICE = 'hw:5'
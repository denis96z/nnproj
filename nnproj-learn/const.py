import os

TYPES = [
    '1992_1', '1992_2',
    '2016_1', '2016_2',
    'unknown',
]

NUM_TYPES = len(TYPES)

SIGN_IMG_WIDTH = 123
SIGN_IMG_HEIGHT = 32

ALPHANUM = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
]

NUM_ALPHANUM_CHARS = len(ALPHANUM)

CHAR_IMG_WIDTH = int(SIGN_IMG_WIDTH * 0.175)
CHAR_IMG_HEIGHT = SIGN_IMG_HEIGHT

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(CUR_DIR, 'data')
CHECK_DIR = os.path.join(CUR_DIR, 'checkpoint')
TF_LOG_DIR = os.path.join(CUR_DIR, 'tensorlog')
KERACT_DIR = os.path.join(CUR_DIR, 'keract')
MODEL_DIR = os.path.join(CUR_DIR, 'model')
PIXELS_DIR = os.path.join(CUR_DIR, 'pixels')

PIXELS_PATH = os.path.join(PIXELS_DIR, 'pixels.py')

BLUE_PX = (0x04, 0x38, 0x9D)
WHITE_PX = (0xD4, 0xE8, 0xFF)
BLACK_PX = (0x22, 0x1A, 0x18)
GREEN_PX = (0x03, 0xB5, 0x5D)
YELLOW_PX = (0xFF, 0xD7, 0x00)

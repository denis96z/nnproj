import os
from random import randint

from PIL import Image, ImageDraw, ImageFont

from const import DATA_DIR
from utils import create_dir

from pixels import pixels

IMG_WIDTH = 185
IMG_HEIGHT = 65

CHAR_WIDTH = int(IMG_WIDTH * 0.17)
CHAR_HEIGHT = IMG_HEIGHT

FONT_SIZE = 58

CHARS = [
    '京', '渝', '沪', '津', '皖', '闽', '粤', '贵', '琼', '冀', '黑', '豫', '鄂', '湘', '苏',
    '赣', '吉', '辽', '青', '陕', '鲁', '晋', '川', '云', '浙', '桂', '蒙', '宁', '藏', '新',
]

NUMBER = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
]

ALFA = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
]

FAKE_DATA_PATH = os.path.join(DATA_DIR, 'naive')

FAKE_TRAIN_PATH = os.path.join(FAKE_DATA_PATH, 'train')
FAKE_TRAIN_PATH_CHINESE_CHARS = os.path.join(FAKE_TRAIN_PATH, 'chinese')
FAKE_TRAIN_PATH_ALPHANUM_CHARS = os.path.join(FAKE_TRAIN_PATH, 'alphanum')

FAKE_TEST_PATH = os.path.join(FAKE_DATA_PATH, 'test')
FAKE_TEST_PATH_CHINESE_CHARS = os.path.join(FAKE_TEST_PATH, 'chinese')
FAKE_TEST_PATH_ALPHANUM_CHARS = os.path.join(FAKE_TEST_PATH, 'alphanum')


CHINESE_FONT = ImageFont.truetype('fonts/chinese.ttf', FONT_SIZE)
ALPHANUM_FONT = ImageFont.truetype('fonts/alphanum.ttf', FONT_SIZE)


def random_offset(x: int, y: int) -> (int, int):
    d = 5
    return randint(x - d, x + d), randint(y - d, y + d)


def create_chinese_char(path: str, c: str, font: object, fgc: tuple, bgc: tuple) -> Image:
    img = Image.new('RGB', (IMG_HEIGHT, IMG_HEIGHT), color=bgc)

    draw = ImageDraw.Draw(img)
    draw.text(random_offset(3, -7), c, fill=fgc, font=font)

    img = img.resize((CHAR_WIDTH, CHAR_HEIGHT), Image.ANTIALIAS)
    img.save(path)


def create_alphanum_char(path: str, c: str, font: object, fgc: tuple, bgc: tuple) -> Image:
    img = Image.new('RGB', (CHAR_WIDTH, CHAR_HEIGHT), color=bgc)

    draw = ImageDraw.Draw(img)
    draw.text(random_offset(3, -7), c, fill=fgc, font=font)

    img.save(path)


def make_iter(s: list):
    idx = 0

    def get_next_item():
        nonlocal idx
        idx = (idx + 1) % len(s)
        return s[idx]

    return get_next_item


def create_char_images(c: str, n: int, font: object,
                       color_sets: list, create: callable,
                       tr_dir_path: str, ts_dir_path: str) -> None:
    idx, ns, nps = 0, len(color_sets), n // len(color_sets)

    fg_next = [make_iter(color_sets[i][0]) for i in range(ns)]
    bg_next = [make_iter(color_sets[i][1]) for i in range(ns)]

    for _ in range(nps):
        for i in range(ns):
            idx += 1
            dir_path = tr_dir_path if idx < (n // 2) else ts_dir_path
            create(os.path.join(dir_path, c, f'{idx}.png'),
                   c, font, fg_next[idx % ns](), bg_next[idx % ns]())

    print(f'PROCESSING COMPLETE: {c}')


def main():
    n = 10000

    for x in CHARS:
        create_dir(os.path.join(FAKE_TRAIN_PATH_CHINESE_CHARS, x))
        create_dir(os.path.join(FAKE_TEST_PATH_CHINESE_CHARS, x))
        create_char_images(x, n, CHINESE_FONT, [
            (pixels.BLACK_PX_SET, pixels.YELLOW_PX_SET),
            (pixels.WHITE_PX_SET, pixels.BLUE_PX_SET),
            (pixels.BLACK_PX_SET, pixels.GREEN_PX_SET),
        ], create_chinese_char, FAKE_TRAIN_PATH_CHINESE_CHARS, FAKE_TEST_PATH_CHINESE_CHARS)
    for x in (ALFA + NUMBER):
        create_dir(os.path.join(FAKE_TRAIN_PATH_ALPHANUM_CHARS, x))
        create_dir(os.path.join(FAKE_TEST_PATH_ALPHANUM_CHARS, x))
        create_char_images(x, n, ALPHANUM_FONT, [
            (pixels.BLACK_PX_SET, pixels.YELLOW_PX_SET),
            (pixels.WHITE_PX_SET, pixels.BLUE_PX_SET),
            (pixels.BLACK_PX_SET, pixels.GREEN_PX_SET),
        ], create_alphanum_char, FAKE_TRAIN_PATH_ALPHANUM_CHARS, FAKE_TEST_PATH_ALPHANUM_CHARS)


main()

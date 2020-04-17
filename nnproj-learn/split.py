import hashlib
import os
import sys
import time

from PIL import Image

SPLIT_PERCENT_1992 = [
    (0.00, 0.16),
    (0.13, 0.28),
    (0.31, 0.46),
    (0.44, 0.59),
    (0.57, 0.72),
    (0.71, 0.86),
    (0.84, 1.00),
]

SPLIT_PERCENT_2016 = [
    (0.00, 0.16),
    (0.15, 0.3),
    (0.31, 0.46),
    (0.43, 0.57),
    (0.53, 0.68),
    (0.63, 0.78),
    (0.75, 0.9),
    (0.86, 1.00),
]


def split_image(src: str, dst_dir: str, split: list) -> None:
    src_img = Image.open(src).convert('RGB')

    sw, sh = src_img.size
    for idx, s in enumerate(split):
        x1, x2 = int(s[0] * sw), min(int(s[1] * sw), sw - 1)
        sgm_img = src_img.crop((x1, 0, x2, sh - 1))

        name = encode_src_path(src)
        sgm_path = os.path.join(dst_dir, f'{name}_{idx}.png')

        sgm_img.save(sgm_path)
        print(f'SEGMENT SAVED: {sgm_path}')


def encode_src_path(src: str) -> str:
    return hashlib.sha224(bytearray(src, encoding='ascii')).hexdigest() + str(round(time.time()))


def main():
    t = sys.argv[1]
    if t == '1992':
        sp = SPLIT_PERCENT_1992
    elif t == '2016':
        sp = SPLIT_PERCENT_2016
    else:
        raise ValueError(f'unknown type {t}')

    # NOTE: path to image, path to destination directory
    src, dst_dir = sys.argv[2], sys.argv[3]
    split_image(src, dst_dir, sp)


main()

#!/usr/bin/env python3
"""USE ONLY FOR ORIGINAL DATASET"""

import os

from PIL import Image, ImageOps

from types import TEST_DATA_PATH, TRAIN_DATA_PATH


def count_d(x: int) -> int:
    c = 1
    x //= 10
    while x > 0:
        x //= 10
        c += 1
    return c


def invert_img(src: str, dst: str) -> None:
    image = Image.open(src)
    if image.mode == 'RGBA':
        r, g, b, a = image.split()

        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)

        r2, g2, b2 = inverted_image.split()
        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

        final_transparent_image.save(dst)
    else:
        inverted_image = ImageOps.invert(image)
        inverted_image.save(dst)


def name_by_idx(path: str, i: int, nx: int) -> str:
    ns = ('{:0' + str(count_d(nx)) + 'd}').format(i)
    return os.path.join(path, ns + '.png')


def prefixed_name(name: str) -> str:
    return f'prefix_{name}'


def rename_image(path: str, old_name: str, new_name: str) -> None:
    os.rename(os.path.join(path, old_name), os.path.join(path, new_name))


def prefix_all_images(path: str, files: list) -> None:
    for fn in files:
        rename_image(path, fn, prefixed_name(fn))


for st_path in [TRAIN_DATA_PATH, TEST_DATA_PATH]:
    path_1, _, files_1 = next(os.walk(os.path.join(st_path, '1992_1')))
    path_2, _, files_2 = next(os.walk(os.path.join(st_path, '1992_2')))

    prefix_all_images(path_1, files_1)
    prefix_all_images(path_2, files_2)

    idx = 0
    n = len(files_1) + len(files_2)

    for f in files_1:
        idx += 1
        f = prefixed_name(f)
        rename_image(path_1, f, name_by_idx(path_1, idx, n))
        invert_img(os.path.join(path_1, f), os.path.join(path_2, name_by_idx(path_2, idx, n)))

    for f in files_2:
        idx += 1
        f = prefixed_name(f)
        rename_image(path_2, f, name_by_idx(path_2, idx, n))
        invert_img(os.path.join(path_2, f), os.path.join(path_1, name_by_idx(path_1, idx, n)))

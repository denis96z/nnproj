import math
import os
import sys

from PIL import Image

from const import BLUE_PX, WHITE_PX, YELLOW_PX, BLACK_PX, GREEN_PX, PIXELS_DIR, PIXELS_PATH
from ptypes import TRAIN_DATA_PATH
from utils import create_dir


def px_diff(px: tuple, norm: tuple) -> float:
    def px_c_sqr(idx):
        return (norm[idx] - px[idx]) ** 2
    return math.sqrt(px_c_sqr(0) + px_c_sqr(1) + px_c_sqr(2))


def list_files(d: str) -> list:
    _, _, files = next(os.walk(d))
    return files


def import_pixels_from_image(path: str, fgc: tuple, bgc: tuple,
                             mxd: float, fg_color_set: set, bg_color_set: set) -> None:
    img = Image.open(path).convert('RGB')
    pxm = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            fgd = px_diff(fgc, pxm[x, y])
            bgd = px_diff(bgc, pxm[x, y])
            if fgd <= mxd:
                fg_color_set.add(pxm[x, y])
            if bgd <= mxd:
                bg_color_set.add(pxm[x, y])
    print(f'PROCESSING COMPLETE: {path}')


def import_pixels_from_images(d: str, fgc: tuple, bgc: tuple,
                              mxd: float, fg_color_set: set, bg_color_set: set) -> None:
    _, _, files = next(os.walk(d))
    for f in files:
        import_pixels_from_image(os.path.join(d, f), fgc, bgc, mxd, fg_color_set, bg_color_set)


def fmt_px_color(v: float) -> str:
    return f'0x{v:02x}'


def fmt_px(px: tuple) -> str:
    return f'({fmt_px_color(px[0])}, {fmt_px_color(px[1])}, {fmt_px_color(px[2])})'


def write_px_to_file(f, px: tuple) -> None:
    f.write(f'\t{fmt_px(px)},\n')


def write_px_set_to_file(f, name: str, pxs: set) -> None:
    f.write(f'{name} = [\n')
    for px in pxs:
        write_px_to_file(f, px)
    f.write(']\n')


def write_px_sets_to_file(green_px_set: set,
                          black_px_set: set, white_px_set: set,
                          blue_px_set: set, yellow_px_set: set,
                          ) -> None:
    create_dir(PIXELS_DIR)
    with open(PIXELS_PATH, 'w') as f:
        write_px_set_to_file(f, 'GREEN_PX_SET', green_px_set)
        write_px_set_to_file(f, 'BLACK_PX_SET', black_px_set)
        write_px_set_to_file(f, 'WHITE_PX_SET', white_px_set)
        write_px_set_to_file(f, 'BLUE_PX_SET', blue_px_set)
        write_px_set_to_file(f, 'YELLOW_PX_SET', yellow_px_set)


def main():
    mxd = float(sys.argv[1])

    green_px_set = set()
    black_px_set, yellow_px_set = set(), set()
    white_px_set, blue_px_set = set(), set()

    import_pixels_from_images(os.path.join(TRAIN_DATA_PATH, '1992_1'), fgc=WHITE_PX, bgc=BLUE_PX, mxd=mxd,
                              fg_color_set=white_px_set, bg_color_set=blue_px_set)
    import_pixels_from_images(os.path.join(TRAIN_DATA_PATH, '1992_2'), fgc=BLACK_PX, bgc=YELLOW_PX, mxd=mxd,
                              fg_color_set=black_px_set, bg_color_set=yellow_px_set)
    import_pixels_from_images(os.path.join(TRAIN_DATA_PATH, '2016_1'), fgc=BLACK_PX, bgc=GREEN_PX, mxd=mxd,
                              fg_color_set=black_px_set, bg_color_set=green_px_set)

    write_px_sets_to_file(green_px_set,
                          black_px_set, white_px_set,
                          blue_px_set, yellow_px_set)


main()

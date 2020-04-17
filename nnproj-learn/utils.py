import pathlib
import shutil

from const import CHECK_DIR, TF_LOG_DIR, KERACT_DIR, CUR_DIR, MODEL_DIR


def create_dir(path: str) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def remove_dir(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)


def create_common_dirs() -> None:
    create_dir(CHECK_DIR)
    create_dir(TF_LOG_DIR)
    create_dir(KERACT_DIR)
    create_dir(MODEL_DIR)


def remove_common_dirs() -> None:
    remove_dir(CHECK_DIR)
    remove_dir(TF_LOG_DIR)
    remove_dir(KERACT_DIR)
    remove_dir(MODEL_DIR)


def create_clean_dir(d: str) -> None:
    remove_dir(d)
    create_dir(d)


def create_clean_common_dirs() -> None:
    remove_common_dirs()
    create_common_dirs()


def relative_path(path: str, cur: str) -> str:
    return path[len(cur) + 1:]


def relative_cur(path: str) -> str:
    return relative_path(path, CUR_DIR)

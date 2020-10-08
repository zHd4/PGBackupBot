import os


def check_root():
    return os.getuid() == 0

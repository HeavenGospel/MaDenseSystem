from configs.setting import load_config
from src.ma_dense_system import start_sys


if __name__ == '__main__':

    start_sys(load_config('config_1'))
    exit(0)
    
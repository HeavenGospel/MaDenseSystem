import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 动态添加项目根目录到 sys.path
from configs.setting import load_config
from src.ma_dense_system import start_sys
from data.input import input

if __name__ == '__main__':
    time_list = input('data\input_data\dense.txt')
    # time_list = input('data\input_data\medium.txt')
    # time_list = input('data\input_data\sparse.txt')
    for time in time_list:
        start_sys(load_config('config_1'), time)
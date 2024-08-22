import sys
import os
from src.calc.get_fuzzy import get_fuzzy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 动态添加项目根目录到 sys.path


def get_compares(df, config, close):
    distance_step = [close * 0.002 * 2, close * 0.0075 * 2, close * 0.015 * 2]
    cross_step = [8 * 2, 5 * 2, 2 * 2.5]
    total_range = config['compare_range'] * 3 + max(config['ma']['sma']['sma3'], config['ma']['ema']['ema3']) + 5
    compares_arr = []
    for i in range(1,4):
        l = total_range - config['compare_range'] * i
        r = total_range - config['compare_range'] * (i-1)
        distance = df.iloc[l:r]['distance'].std()
        cross = df.iloc[l:r]['cross'].sum()
        compares_arr.append(get_fuzzy(distance, distance_step, cross, cross_step))
    return compares_arr


    
# 历史比较模型
import sys
import os
from src.calc.get_fuzzy import get_fuzzy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 动态添加项目根目录到 sys.path


def get_compares(df, config):
    
    compares = []
    flag = config['compare_range'] * 3 + max(config['ma']['sma']['sma3'], config['ma']['ema']['ema3']) + 5 - 1
    distance_step = [config['fuzzy']['distance']['step1'], config['fuzzy']['distance']['step2']]
    cross_step = [config['fuzzy']['cross']['step1'] * 3, config['fuzzy']['cross']['step2'] * 3]
    slope_step = [config['fuzzy']['slope']['step1'], config['fuzzy']['slope']['step2']]
    
    for i in range(1,4):
        l = flag - config['compare_range'] * i
        r = flag - config['compare_range'] * (i-1)
        distance = df.iloc[l:r]['distance'].mean()
        cross = df.iloc[l:r]['cross'].sum()
        slope = df.iloc[l:r]['slope'].mean()
        print("标准差, 交叉点, 斜率:")
        print(distance, cross, slope)
        compares.append(get_fuzzy(distance, distance_step, cross, cross_step, slope, slope_step))
    return compares


    
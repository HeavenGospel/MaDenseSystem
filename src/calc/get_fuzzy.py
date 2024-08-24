# 模糊数学模型
import numpy as np


# 模糊化函数
def fuzzify1(value, step):
    if value < step[0]:
        return 1.0
    elif step[0] <= value <= step[1]:
        return (step[1] - value) / (step[1] - step[0])
    else:  # value > step[1]
        return 0.0
    
def fuzzify2(value, step):
    if value < step[0]:
        return 0.0
    elif step[0] <= value <= step[1]:
        return (value - step[0]) / (step[1] - step[0])
    else:  # value > step[1]
        return 1.0

# 计算密集度的函数
def get_fuzzy(distance, distance_step, cross, cross_step, slope, slope_step):

    # 模糊化过程
    fuzzy_distance = fuzzify1(distance, distance_step)
    fuzzy_cross = fuzzify2(cross, cross_step)
    fuzzy_slope = fuzzify1(slope, slope_step)
    
    # 规则：密集度 = (fuzzy_distance * 0.5 + fuzzy_cross * 0.3 + fuzzy_slope * 0.2)
    fianl_density = (fuzzy_distance * 0.5 + fuzzy_cross * 0.3 + fuzzy_slope * 0.2)
    
    return float(fianl_density)

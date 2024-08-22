import numpy as np

def fuzzify_std_deviation(std_dev, step):
    if std_dev < step[0]:
        return {"good": 1.0, "medium": 0.0, "bad": 0.0}
    elif step[0] <= std_dev < step[1]:
        return {
            "good": (step[1] - std_dev) / (step[1] - step[0]),
            "medium": (std_dev - step[0]) / (step[1] - step[0]),
            "bad": 0.0
        }
    elif step[1] <= std_dev <= step[2]:
        return {
            "good": 0.0,
            "medium": (step[2] - std_dev) / (step[2] - step[1]),
            "bad": (std_dev - step[1]) / (step[2] - step[1])
        }
    else:
        return {"good": 0.0, "medium": 0.0, "bad": 1.0}

def fuzzify_num_crossovers(crossovers, step):
    if crossovers > step[0]:
        return {"good": 1.0, "medium": 0.0, "bad": 0.0}
    elif step[0] >= crossovers >= step[1]:
        return {"good": (step[1] - crossovers) / (step[1] - step[0]), "medium": (crossovers - step[0]) / (step[1] - step[0]), "bad": 0.0}
    elif step[1] >= crossovers >= step[2]:
        return {"good": 0.0, "medium": (step[2] - crossovers) / (step[2] - step[1]), "bad": (crossovers - step[1]) / (step[2] - step[1])}
    else:
        return {"good": 0.0, "medium": 0.0, "bad": 1.0}

# 去模糊化 - 重心法
def defuzzify(density):
    # 假设 good = 3, medium = 2, bad = 1 的值
    values = {"good": 3, "medium": 2, "bad": 1}
    numerator = sum(density[key] * values[key] for key in density)
    denominator = sum(density.values())
    return numerator / denominator if denominator != 0 else 0

def get_fuzzy(distance, distance_step, cross, cross_step):

    # 模糊化过程
    fuzzy_std = fuzzify_std_deviation(distance, distance_step)
    fuzzy_crossovers = fuzzify_num_crossovers(cross, cross_step)

    # 定义模糊规则并计算隶属度
    density = {
        "good": min(fuzzy_std["good"], fuzzy_crossovers["good"]),
        "medium": min(fuzzy_std["medium"], fuzzy_crossovers["medium"]),
        "bad": min(fuzzy_std["bad"], fuzzy_crossovers["bad"])
    }

    # 计算最终的密集度值
    final_density = defuzzify(density)
    return final_density
    # print(f"标准差隶属度: {fuzzy_std}")
    # print(f"交叉点隶属度: {fuzzy_crossovers}")
    # print(f"密集度隶属度: {density}")
    # print(f"最终密集度: {final_density}")

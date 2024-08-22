# 交叉点模型
import numpy as np
import pandas as pd


def get_cross(df, ma_params):
    # 计算两条均线的差值
    df_cross = pd.DataFrame()
    ma_minus_name = []
    for i in range(len(ma_params)):
        for j in range(i+1, len(ma_params)):
            ma_minus_name.append(ma_params[i][1] + '_' + ma_params[j][1])
            df_cross[ma_minus_name[-1]] = df[ma_params[i][1]] - df[ma_params[j][1]]

    # 判断交叉点：
    df['cross'] = 0
    for minus_name in ma_minus_name:
        df['cross'] += np.where(df_cross[minus_name] * df_cross[minus_name].shift(1) <= 0, 1, 0)

    # # 设定阈值，例如在10*15分钟内有10次以上交叉
    # threshold = 10
    # # 判断是否密集
    # df['is_dense'] = df['cross_count'] > threshold
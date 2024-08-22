# 标准差模型
import pandas as pd


def get_distance(df, ma_params):
    df_distance = pd.DataFrame()
    ma_diff_name = []
    for i in range(len(ma_params)):
        for j in range(i+1, len(ma_params)):
            ma_diff_name.append(ma_params[i][1] + '_' + ma_params[j][1])
            df_distance[ma_diff_name[-1]] = abs(df[ma_params[i][1]] - df[ma_params[j][1]])
    # 计算每条均线之间间距的标准差
    df['distance'] = df_distance[ma_diff_name].std(axis=1)
    
    # 计算每条均线之间间距的方差
    # df['distance_var'] = df_distance[ma_diff_name].var(axis=1)

    # # 设定一个密集度方差的阈值
    # var_threshold = 0.000025  # 假设是价格的0.0025%
    # # 判断密集度
    # df['is_dense_by_var'] = df['distance_var'] < var_threshold
    # # 设定一个密集度标准差的阈值
    # std_threshold = 0.005
    # # 判断密集度
    # df['is_dense_by_std'] = df['distance_std'] < std_threshold
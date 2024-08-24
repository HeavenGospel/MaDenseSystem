# 斜率模型
import pandas as pd


def get_slope(df, ma_params):
    df_slope = pd.DataFrame()
    ma_slope_name = []

    for i in range(len(ma_params)):
        ma_slope_name.append(ma_params[i][1] + '_slope')
        df_slope[ma_slope_name[-1]] = abs(df[ma_params[i][1]].diff())

    # 计算斜率差异的平均值或标准差或方差
    df['slope'] = df_slope[ma_slope_name].mean(axis=1)

    # # 设定密集度阈值
    # slope_diff_threshold = 0.00001  # 根据实际数据范围设定
    # # 判断均线是否密集
    # df['is_dense'] = df['slope_diff_avg'] < slope_diff_threshold
    
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def calculate_slope(series):
    series = series.dropna()  # 移除NaN值
    if len(series) < 2:
        return np.nan  # 不足数据点时返回NaN
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    return model.coef_[0][0]

def slope_to_radian(slope):
    return np.arctan(slope)

def calculate_angle_difference(radian1, radian2):
    diff = np.abs(radian1 - radian2)
    return min(diff, 2 * np.pi - diff)

def get_slope(df, ma_params):
    df_slope = pd.DataFrame()
    ma_slope_name = []
        
    for i in range(len(ma_params)):
        for j in range(i+1, len(ma_params)):
            ma1_name = ma_params[i][1]
            ma2_name = ma_params[j][1]
            ma_slope_name.append(ma_params[i][1] + '_' + ma_params[j][1])
            
            angle_differences = []
            
            for k in range(len(df)):
                if k >= max(df[ma1_name].first_valid_index(), df[ma2_name].first_valid_index()):
                    ma1_slope = calculate_slope(df[ma1_name].iloc[max(0, k - len(df[ma1_name].dropna()) + 1):k + 1])
                    ma2_slope = calculate_slope(df[ma2_name].iloc[max(0, k - len(df[ma2_name].dropna()) + 1):k + 1])
                    
                    radian_ma1 = slope_to_radian(ma1_slope)
                    radian_ma2 = slope_to_radian(ma2_slope)
                    
                    angle_diff = calculate_angle_difference(radian_ma1, radian_ma2)
                else:
                    angle_diff = np.nan
                
                angle_differences.append(angle_diff)
            
            df_slope[ma_slope_name[-1]] = angle_differences

    # 计算标准差
    df['slope'] = df_slope[ma_slope_name].std(axis=1)



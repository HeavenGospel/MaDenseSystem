# 计算Ma均线


def get_ma(df, ma_params):
    # 计算简单移动平均线 (SMA)
    for ma in ma_params:
        if ma[0] == 0:
            df[ma[1]] = df['close'].rolling(window=ma[2]).mean()
        else:
            df[ma[1]] = df['close'].ewm(span=ma[2], adjust=True, min_periods=ma[2]).mean()
    return df

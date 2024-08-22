import os
import sys
import math
import ccxt
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 动态添加项目根目录到 sys.path
from src.utils.time_to_sec import time_to_sec
from src.calc.get_ma import get_ma
from src.calc.get_distance import get_distance
from src.calc.get_cross import get_cross
from src.calc.get_compares import get_compares
from src.calc.get_fuzzy import get_fuzzy

def start_sys(config):
    # region 配置参数
    # 创建交易所对象
    exchange = getattr(ccxt, config['exchange_name']) (config['exchange_params'])
    
    # 获取时间周期长度, 单位秒
    timeframe_sec = time_to_sec(config['timeframe'])
    # 获取当前时间戳
    now_timestamp = datetime.now().timestamp();
    # 获取系统启动时间(系统启动时间为时间周期的整数倍, 且比当前时间戳小)
    sys_start_time = datetime.fromtimestamp((now_timestamp - now_timestamp % timeframe_sec)).strftime('%Y-%m-%d %H:%M:%S')
    #sys_start_time = '2024-08-22 06:30:00'

    # 结束时间为系统启动时间转换为毫秒级时间戳
    end_timestamp = int(datetime.strptime(sys_start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    # 总区间的长度
    total_range = config['compare_range'] * 3 + max(config['ma']['sma']['sma3'], config['ma']['ema']['ema3']) + 5
    # 总区间的时间步长
    step = timeframe_sec * 1000 * (total_range - 1)
    # 开始时间由结束时间和时间长度得出
    start_timestamp = end_timestamp - step
    # endregion

    # region 获取k线数据
    ohlcv = exchange.fetch_ohlcv(symbol=config['symbol'], since=start_timestamp,timeframe=config['timeframe'], limit=total_range)
    # 将数据转为 DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # 将时间戳转换为 UTC+8 时间
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
    sys_start_close = df.iloc[-1]['close']
    # endregion
    
    # region 获取均线
    # 均线命名
    ma_params = []
    for id in config['ma']['sma']:
        name = 'sma' + str(config['ma']['sma'][id])
        value = config['ma']['sma'][id]
        ma_params.append([0, name, value])
    for id in config['ma']['ema']:
        name = 'ema' + str(config['ma']['ema'][id])
        value = config['ma']['ema'][id]
        ma_params.append([1, name, value])
    # 计算均线
    get_ma(df, ma_params)
    # endregion
    
    # region 模型计算
    get_distance(df, ma_params)  # 获取标准差
    get_cross(df, ma_params)  # 获取交叉点
    # get_slope(df, ma_params)  # 获取斜率, 斜率效果不好且计算量大, 弃用
    
    distance = df.iloc[total_range - 10:]['distance'].std()
    cross = df.iloc[total_range - 10:]['cross'].sum()
    
    # 模糊数学还未成熟, 弃用
    # distance_step = [sys_start_close * 0.002, sys_start_close * 0.0075, sys_start_close * 0.015]
    # cross_step = [8, 5, 2]
    # fuzzy_result = get_fuzzy(distance, distance_step, cross,cross_step)
    
    # compares = get_compares(df, config, sys_start_close)  # 获取历史比较数据
    # if (compares[0] < compares[1]) and (compares[0] < compares[2]):
    #     fuzzy_result *= 1.2
    # elif (compares[0] < compares[1]) or (compares[0] < compares[2]):
    #     fuzzy_result *= 0.8
    # else:
    #     fuzzy_result *= 1
    # endregion

    # region 输出数据
    # print('历史比较数据:', compares)
    print('系统启动时间:', sys_start_time)
    print('标准差:', distance)
    print('交叉点:', cross)
    print('密集度:', (sys_start_close - distance * distance * math.sqrt(distance)) / sys_start_close + cross / 30)
    # df = df.drop(['open', 'high', 'low', 'volume'], axis=1)  # 去掉一些列
    # df.iloc[121:].to_excel('ma_dense_system.xlsx', index=False)  # 输出exel
    # endregion
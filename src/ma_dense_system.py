import os
import sys
import ccxt
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 动态添加项目根目录到 sys.path
from src.utils.time_to_sec import time_to_sec
from src.calc.get_ma import get_ma
from src.calc.get_distance import get_distance
from src.calc.get_cross import get_cross
from src.calc.get_slope import get_slope
from src.calc.get_compares import get_compares
from src.calc.get_fuzzy import get_fuzzy
from src.operations.send_msg import send_msg

def start_sys(config, sys_start_time = ''):
    # region 配置参数
    # 创建交易所对象
    exchange = getattr(ccxt, config['exchange_name']) (config['exchange_params'])
    
    # 获取时间周期长度, 单位秒
    timeframe_sec = time_to_sec(config['timeframe'])
    # 获取当前时间戳
    now_timestamp = datetime.now().timestamp();
    # 获取系统启动时间(系统启动时间为时间周期的整数倍, 且比当前时间戳小)
    if sys_start_time == '':
        sys_start_time = datetime.fromtimestamp((now_timestamp - now_timestamp % timeframe_sec)).strftime('%Y-%m-%d %H:%M:%S')

    # 结束时间为系统启动时间转换为毫秒级时间戳
    end_timestamp = int(datetime.strptime(sys_start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    # 总区间的长度
    total_range = config['main_range'] + config['compare_range'] * 3 + max(config['ma']['sma']['sma3'], config['ma']['ema']['ema3']) + 5
    # 总区间的时间步长
    step = timeframe_sec * 1000 * (total_range - 1)
    # 开始时间由结束时间和时间长度得出
    start_timestamp = end_timestamp - step
    # endregion

    # region 获取k线数据
    try:
        ohlcv = exchange.fetch_ohlcv(symbol=config['symbol'], since=start_timestamp,timeframe=config['timeframe'], limit=total_range)
        print('获取k线数据成功')
    except Exception as e:
        print('获取k线数据失败:', e)
        print('==============================')
        return
    # 将数据转为 DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # 将时间戳转换为 UTC+8 时间
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
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
    get_slope(df, ma_params)  # 获取斜率
    
    distance = df.iloc[total_range - config['main_range']:]['distance'].min()
    cross = df.iloc[total_range - config['main_range']:]['cross'].sum()
    slope = df.iloc[total_range - config['main_range']:]['slope'].mean()
    
    # 模糊数学计算
    fuzzy_result = get_fuzzy(
                            distance, [config['fuzzy']['distance']['step1'], config['fuzzy']['distance']['step2']], 
                            cross, [config['fuzzy']['cross']['step1'], config['fuzzy']['cross']['step2']],
                            slope, [config['fuzzy']['slope']['step1'], config['fuzzy']['slope']['step2']],
                            )
    
    # 历史比较, 暂时未优化好, 弃用
    # compares = get_compares(df, config)  # 获取历史比较数据
    # compare_result = (
    #     (fuzzy_result - compares[0]) + 
    #     (fuzzy_result - compares[1]) + 
    #     (fuzzy_result - compares[2])
    # )
    # endregion

    # region 输出数据
    print('系统启动时间:', sys_start_time)
    print('标准差:', distance)
    print('交叉点:', cross)
    print('斜率:', slope)
    print('模糊数学计算结果:', fuzzy_result)
    # print('历史比较:', compares)
    # print('历史比较结果:', compare_result)
    # print('最终结果:', compare_result * 0.7 + fuzzy_result * 0.3)
    
    # file_name = sys_start_time.replace(':', '_') + '.xlsx'
    # df = df.drop(['open', 'high', 'low', 'volume'], axis=1)  # 去掉一些列
    # df.iloc[total_range - config['compare_range'] * 3:].to_excel(file_name, index=False)  # 输出exel
    # print('数据输出完成')

    if fuzzy_result >= 0.7:
        send_msg();

    print('==============================')
    # endregion

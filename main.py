from time import time
from configs.setting import load_config
from src.ma_dense_system import start_sys
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def your_function():
    # 你需要运行的代码
    print(f"Running function at {datetime.now()}")

if __name__ == '__main__':
    print("Starting scheduler...")
    # 创建调度器
    scheduler = BlockingScheduler()

    # 每15分钟运行一次任务
    scheduler.add_job(start_sys, 'interval', minutes=15, start_date=datetime.now(), args=[load_config('config_1')])

    # 启动调度器
    try:
        print("Scheduler started. Running every 15 minutes.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

    exit(0)
    
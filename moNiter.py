import asyncio
from sensor_reader import read_sensor_data  # 假设主文件名为sensor_reader.py
import datetime


async def monitor(interval_minutes=5):
    """定时读取传感器数据"""
    while True:
        print(f"\n{'-' * 40}")
        print(f"开始读取 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await read_sensor_data()

        # 等待指定分钟
        await asyncio.sleep(interval_minutes*60)


if __name__ == "__main__":
    # 每5分钟读取一次
    asyncio.run(monitor(5))
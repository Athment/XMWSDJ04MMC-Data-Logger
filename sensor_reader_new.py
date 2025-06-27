import asyncio
from bleak import BleakClient
import struct
import datetime
import csv

# 设备配置
DEVICE_ADDRESS = "04:0d:84:c2:56:e8"  # 替换为你的设备MAC地址
SERVICE_UUID = "ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6"
CHAR_UUID = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"
interval_minutes = 5

def parse_sensor_data(data):
    """解析温湿度原始数据"""
    if len(data) < 4:
        raise ValueError(f"无效数据长度: {len(data)} bytes")

    # 解析数据 (小端序格式)
    # 温度：前2字节，有符号整数，单位0.1℃
    # 湿度：后2字节，无符号整数，单位0.1%
    temp_raw = struct.unpack('<h', data[:2])[0]  # 有符号短整型
    hum_raw = struct.unpack('<H', data[2:4])[0]  # 无符号短整型

    # 转换为实际值
    temperature = temp_raw / 10.0
    humidity = hum_raw / 10.0

    # 解析电池电量（如果存在）
    battery = data[4] if len(data) >= 5 else None

    return temperature, humidity, battery


def save_to_csv(timestamp, temp, hum, batt):
    """保存数据到CSV文件"""
    filename = "sensor_data.csv"
    try:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            # 如果文件是新建的，写入表头
            if f.tell() == 0:
                writer.writerow(["Timestamp", "Temperature(℃)", "Humidity(%)", "Battery(%)"])

            writer.writerow([timestamp, f"{temp:.1f}", f"{hum:.1f}", batt])
        print(f"数据已保存到 {filename}")
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")


async def read_sensor_data():
    """连接设备并读取传感器数据"""
    print(f"尝试连接设备: {DEVICE_ADDRESS}")
    client = None

    try:
        # 连接设备
        client = BleakClient(DEVICE_ADDRESS)
        await client.connect(timeout=15.0)
        print("设备连接成功!")

        # 检查服务是否可用
        services = await client.get_services()
        if SERVICE_UUID not in [str(s.uuid) for s in services]:
            print(f"错误: 设备未提供所需服务 {SERVICE_UUID}")
            return None

        # 循环读取保证蓝牙不断
        while True:
            # 读取特征值
            raw_data = await client.read_gatt_char(CHAR_UUID)
            print(f"原始数据: {raw_data.hex()}")

            # 解析数据
            temp, hum, batt = parse_sensor_data(raw_data)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 显示结果
            print("\n===== 传感器读数 =====")
            print(f"时间: {timestamp}")
            print(f"温度: {temp:.1f}℃")
            print(f"湿度: {hum:.1f}%")
            if batt is not None:
                print(f"电池电量: {batt}%")
            print("=====================")

            # 保存到CSV
            save_to_csv(timestamp, temp, hum, batt)
            await asyncio.sleep(interval_minutes*60)

        return temp, hum, batt

    except Exception as e:
        print(f"错误: {str(e)}")
        return None
    finally:
        if client and client.is_connected:
            await client.disconnect()
            print("设备已断开连接")



def setup_windows_bluetooth():
    """Windows蓝牙设置指南"""
    print("\n重要提示：在Windows上使用蓝牙需要以下准备：")
    print("1. 确保您的电脑支持蓝牙4.0或更高版本")
    print("2. 在Windows设置中打开蓝牙功能")
    print("3. 安装最新版蓝牙驱动程序")
    print("4. 可能需要运行以下命令启用WinRT API:")
    print("   PowerShell命令: Set-ExecutionPolicy Unrestricted -Scope CurrentUser")
    print("5. 确保设备未被其他程序占用（如手机APP）")


if __name__ == "__main__":
    # 显示设置指南
    setup_windows_bluetooth()

    # 运行异步函数
    print("\n开始读取传感器数据...")
    asyncio.run(read_sensor_data())

    # 提示后续操作
    print("\n提示：要定期读取数据，可以将此脚本添加到Windows任务计划程序")
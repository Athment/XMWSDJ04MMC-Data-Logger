# utf-8
import pandas as pd
import matplotlib.pyplot as plt

# 设置plt显示中文
plt.rcParams["font.sans-serif"] = ["SimHei"]


# 读取数据
df = pd.read_csv("sensor_data.csv", parse_dates=["Timestamp"], encoding="gbk")

# 创建图表
plt.figure(figsize=(12, 6))
plt.plot(df["Timestamp"], df["Temperature(℃)"], label="温度(℃)")
plt.plot(df["Timestamp"], df["Humidity(%)"], label="湿度(%)")

# 添加标签
plt.title("温湿度变化趋势")
plt.xlabel("时间")
plt.ylabel("数值")
plt.legend()
plt.grid(True)

# 保存图表
plt.savefig("sensor_data.png")
plt.show()
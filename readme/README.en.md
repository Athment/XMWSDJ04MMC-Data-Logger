en [English](readme/README.en.md) | zh [简体中文](README.md)

# XMWSDJ04MMC-Data-Logger
# Xiaomi Electronic Thermometer and Hygrometer Data Logger

![Sensor Data Visualization](sensor_data.png)

## Project Overview

Xiaomi TH Monitor is a toolkit for monitoring data from the Xiaomi Electronic Thermometer and Hygrometer (XMWSDJ04MMC). It collects temperature and humidity data in real-time via Bluetooth Low Energy (BLE) technology, stores it in CSV format, and provides data visualization capabilities.

Core Features:
- 📡 Bluetooth connection to Xiaomi thermometer and hygrometer for real-time data reading
- 💾 Automatically save data to CSV files
- 📊 Generate temperature and humidity trend charts
- ⏱️ Support scheduled automatic data collection
- 🔋 Battery level monitoring

## Supported Devices

This project is specifically developed for **Xiaomi Electronic Thermometer and Hygrometer 2 (XMWSDJ04MMC)**

## Functional Components

| File | Description |
|------|-------------|
| `sensor_reader.py` | Core module for Bluetooth connection and data reading |
| `monitor.py` | Scheduled data collection script | Deprecated, functionality merged into sensor_reader.py
| `viewer.py` | Data visualization tool | Editable |
| `sensor_data.csv` | Data storage file |

## Installation and Configuration

### Prerequisites
- Python 3.7+
- Windows 10/11 or Linux system
- Bluetooth 4.0+ adapter
- Xiaomi Thermometer and Hygrometer (XMWSDJ04MMC)

### Installation Steps

1. Clone repository:
   ```bash
   git clone https://github.com/Athment/XMWSDJ04MMC-Data-Logger.git
   cd XMWSDJ04MMC-Data-Logger
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
```

3. Windows Bluetooth setup (Windows only):
   - Ensure Bluetooth is enabled
   - Install latest Bluetooth drivers
   - Run PowerShell as administrator:
     ```powershell
     Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```

## Usage Instructions

### 1. Single Data Collection
```bash
python sensor_reader.py
```

### 2. Scheduled Monitoring (every 5 minutes) (Deprecated)
```bash
python monitor.py
```

### 3. Scheduled Monitoring (every 5 minutes)
```bash
python sensor_reader_new.py
```

Data will be saved to `sensor_data.csv`

### 4. Data Visualization
```bash
python viewer.py
```

Generated charts will be saved as `sensor_data.png`

## File Descriptions

### `sensor_reader.py`
Core Bluetooth data collection module:
- Automatically connects to Xiaomi thermometer/hygrometer
- Parses temperature, humidity and battery data
- Saves data to CSV file
- Provides Windows Bluetooth setup guide

### `sensor_reader_new.py`
Scheduled data collection script:
- Configurable collection interval (default 10 minutes)
- Continuous operation mode
- Integrated data collection logging

### `viewer.py`
Data visualization tool:
- Reads CSV data files
- Generates temperature and humidity trend charts
- Supports Chinese titles and labels
- Automatically saves as PNG image

### `sensor_data.csv`
Data storage format:
```csv
Timestamp,Temperature(℃),Humidity(%),Battery(%)
2025-06-26 19:12:32,25.8,59.0,113
2025-06-26 19:18:10,25.8,58.5,105
...
```

## Technical Details

### Data Parsing
Xiaomi thermometer/hygrometer uses custom BLE characteristic values for data transmission:
```python
def parse_sensor_data(data):
    # First 2 bytes: temperature (signed integer, unit 0.1°C)
    # Next 2 bytes: humidity (unsigned integer, unit 0.1%)
    # 5th byte: battery level (optional)
    temp_raw = struct.unpack('<h', data[:2])[0]
    hum_raw = struct.unpack('<H', data[2:4])[0]
    temperature = temp_raw / 10.0
    humidity = hum_raw / 10.0
    battery = data[4] if len(data) >= 5 else None
    return temperature, humidity, battery
```

### Bluetooth Parameters
| Parameter           | Value                                  |
| ------------------- | -------------------------------------- |
| Service UUID        | `ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6` |
| Characteristic UUID | `ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6` |

## Important Notes

1. **Device Connection**:
   - Ensure the device is within Bluetooth range (approx. 10m)
   - Manual pairing may be required for first-time use
   - Device MAC address can be configured in code

2. **Windows Bluetooth Limitations**:
   - Administrator privileges may be required
   - Avoid multiple programs accessing Bluetooth simultaneously
   - Restart Bluetooth service if connection fails

3. **Battery Optimization**:
   - Device battery life ≈1 year (CR2032)
   - Frequent readings accelerate battery consumption
   - Recommended monitoring interval ≥5 minutes

## Explanation
- Device MAC address needs to be obtained from Mi Home or other sources
- The deprecated monitor.py's scheduled function disconnects Bluetooth, requiring manual restart
- sensor_reader_new.py collects and saves data every 5 minutes without disconnecting Bluetooth. Stop collection by interrupting the code

## Contribution Guidelines

Welcome to contribute via Issues or Pull Requests:
1. Submit new feature suggestions or problem reports
2. Create branch for new feature development
3. Ensure code complies with PEP8 standards
4. Update relevant documentation

---

**Make Environmental Monitoring Smarter** - Build professional monitoring systems with Xiaomi devices and Python!
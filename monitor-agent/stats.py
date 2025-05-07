import json
import psutil
import platform
import socket
import time
import subprocess
from datetime import timedelta

def get_ping(host="8.8.8.8"):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", host],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "time=" in line:
                    return float(line.split("time=")[-1].split()[0])
    except:
        pass
    return None

def get_bandwidth(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    rx_bytes = net2.bytes_recv - net1.bytes_recv
    tx_bytes = net2.bytes_sent - net1.bytes_sent

    rx_speed = round(rx_bytes / 1024 / 1024 / interval, 2)  # MB/s
    tx_speed = round(tx_bytes / 1024 / 1024 / interval, 2)  # MB/s

    return rx_speed, tx_speed

def get_stats():
    boot_time = psutil.boot_time()
    uptime = str(timedelta(seconds=(time.time() - boot_time)))
    rx_speed, tx_speed = get_bandwidth()

    stats = {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "uptime": uptime,
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "usage_percent": psutil.cpu_percent(interval=1)
        },
        "memory": {
            "total_mb": round(psutil.virtual_memory().total / 1024**2, 2),
            "used_mb": round(psutil.virtual_memory().used / 1024**2, 2),
            "usage_percent": psutil.virtual_memory().percent
        },
        "swap": {
            "total_mb": round(psutil.swap_memory().total / 1024**2, 2),
            "used_mb": round(psutil.swap_memory().used / 1024**2, 2),
            "usage_percent": psutil.swap_memory().percent
        },
        "disk": [],
        "network_interfaces": [],
        "network": {
            "total_rx_mb": round(psutil.net_io_counters().bytes_recv / 1024 / 1024, 2),
            "total_tx_mb": round(psutil.net_io_counters().bytes_sent / 1024 / 1024, 2),
            "rx_speed_mbps": rx_speed,
            "tx_speed_mbps": tx_speed
        },
        "ping": get_ping()
    }

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            stats["disk"].append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total_gb": round(usage.total / 1024**3, 2),
                "used_gb": round(usage.used / 1024**3, 2),
                "usage_percent": usage.percent
            })
        except PermissionError:
            continue

    net_io = psutil.net_io_counters(pernic=True)
    for interface, data in net_io.items():
        stats["network_interfaces"].append({
            "interface": interface,
            "rx_mb": round(data.bytes_recv / 1024 / 1024, 2),
            "tx_mb": round(data.bytes_sent / 1024 / 1024, 2),
            "packets_sent": data.packets_sent,
            "packets_recv": data.packets_recv
        })

    return stats

if __name__ == "__main__":
    print(json.dumps(get_stats()))

# /opt/monitor-agent.py

import psutil
import platform
import subprocess
import json

def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    try:
        ping = subprocess.check_output(["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                                       stderr=subprocess.DEVNULL).decode()
        latency = float(ping.split("time=")[-1].split(" ms")[0])
    except Exception:
        latency = -1

    return {
        "cpu": cpu,
        "ram": {"total": ram.total, "used": ram.used, "percent": ram.percent},
        "disk": {"total": disk.total, "used": disk.used, "percent": disk.percent},
        "network": {"sent": net.bytes_sent, "recv": net.bytes_recv},
        "ping": latency,
        "os": platform.system()
    }

if __name__ == "__main__":
    print(json.dumps(get_stats()))

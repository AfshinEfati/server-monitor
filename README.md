📚 زبان‌ها: [🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md)
# 📊 Server Monitor Dashboard by Afshin



This system is designed for real-time monitoring of server resources. It consists of two main components:

- **Frontend**: Web dashboard built with Nuxt and TailwindCSS
- **Backend**: API built with FastAPI and a lightweight agent (stats.py) for monitored servers

---

## ✨ Features

- View, add, edit, and delete server records
- Live monitoring of CPU, RAM, Disk, Load Avg, OS version, and Uptime
- Realtime Ping status and network traffic
- Live RX / TX network charts
- Automatic updates every 5 seconds
- Lightweight and no dependency on external services

---

## ⚙️ Requirements

- Linux OS (Ubuntu preferred)
- Python 3.10+
- Node.js and pnpm
- Root access for service installation

---

## 🧠 Backend Installation

### Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Create virtual environment and install packages

```bash
cd /opt/server-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create systemd service for backend

```bash
sudo nano /etc/systemd/system/monitor-backend.service
```

Service content:

```ini
[Unit]
Description=Monitor Backend Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/server-monitor
ExecStart=/opt/server-monitor/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8042
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### Enable and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable monitor-backend.service
sudo systemctl start monitor-backend.service
```

---

## 🌐 Frontend Installation

To deploy the frontend, simply run the script:

```bash
chmod +x frontend/deploy.sh
frontend/deploy.sh
```

This script will:
- Install packages
- Build the project
- Copy the output to the destination path

---

## 📡 Server Agent (stats.py)

To monitor other servers, install `stats.py` on each destination server:

```bash
ssh user@destination-server "mkdir -p /opt/monitor-server"
scp /opt/monitor-server/stats.py user@destination-server:/opt/monitor-server/stats.py
```


---

🧑‍💻 Developed by: Afshin

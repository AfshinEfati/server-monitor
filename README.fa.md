📚 Languages: [🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md)
# 📊 داشبورد مانیتورینگ سرور

این سیستم برای مانیتورینگ زنده منابع سرورها طراحی شده است. شامل دو بخش اصلی است:

- **Frontend**: رابط کاربری تحت وب با استفاده از Nuxt و TailwindCSS
- **Backend**: API سریع با FastAPI و اسکریپت Agent برای سرورهای مانیتور شونده

---

## ✨ امکانات

- مشاهده لیست سرورها + افزودن، ویرایش و حذف آن‌ها
- نمایش زنده مصرف CPU، RAM، Disk، Load Average، نسخه سیستم عامل، زمان روشن بودن سیستم و ...
- مشاهده وضعیت Ping و ترافیک لحظه‌ای شبکه
- نمایش نمودار زنده RX / TX شبکه
- بروزرسانی اطلاعات هر ۵ ثانیه یک‌بار به‌صورت خودکار
- بسیار سبک و بدون نیاز به سرویس‌های خارجی

---

## ⚙️ پیش‌نیازها

- سیستم عامل لینوکس (ترجیحاً Ubuntu)
- Python 3.10 یا بالاتر
- Node.js و pnpm
- دسترسی root برای نصب سرویس

---

## 🧠 نصب Backend

### نصب وابستگی‌ها

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### ساخت محیط مجازی و نصب پکیج‌ها

```bash
cd /opt/server-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ساخت سرویس systemd برای اجرای Backend

```bash
sudo nano /etc/systemd/system/monitor-backend.service
```

محتوای فایل:

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

### فعال‌سازی و اجرای سرویس

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable monitor-backend.service
sudo systemctl start monitor-backend.service
```

---

## 🌐 نصب Frontend

برای دیپلوی فرانت‌اند کافی‌ست اسکریپت زیر را اجرا کنید:

```bash
chmod +x frontend/deploy.sh
frontend/deploy.sh
```

این اسکریپت به‌صورت خودکار:
- پکیج‌ها را نصب می‌کند
- پروژه را build می‌کند
- خروجی را در مسیر نهایی کپی می‌کند

---

## 📡 Agent روی سرورهای دیگر (stats.py)

برای دریافت اطلاعات منابع از سایر سرورها، باید فایل `stats.py` را روی سرور مقصد نصب کنید:

```bash
ssh user@destination-server "mkdir -p /opt/monitor-server"
scp /opt/monitor-server/stats.py user@destination-server:/opt/monitor-server/stats.py
```


---

🧑‍💻 توسعه داده‌شده توسط: افشین

# 🎮 MINECRAFT SERVER MANAGER - TERMUX SETUP

## For Android Termux Users

### 📱 Quick Setup

```bash
# 1. Install Termux from F-Droid (NOT Play Store!)
# Download: https://f-droid.org/packages/com.termux/

# 2. Update Termux
pkg update && pkg upgrade

# 3. Navigate to project
cd ~/minecraft-server-manager

# 4. Run installation
bash install.sh

# 5. Start manager
bash msm.sh
```

---

## ⚠️ Common Termux Issues & Fixes

### Issue 1: Menu Loops Back
**Fix:** The menu now waits for Enter key press after each operation.

### Issue 2: Server Won't Start
**Causes:**
- Java not installed
- Not enough RAM
- Port already in use

**Fix:**
```bash
# Check Java
java -version

# If not installed:
pkg install openjdk-17

# Check available RAM
free -m

# Kill any stuck processes
pkill -f java
```

### Issue 3: Web Dashboard Won't Start
**Fix:**
```bash
# Install Flask
pip install flask flask-cors

# Or use system packages
pkg install python-flask

# Then start
python core/web_panel.py
```

### Issue 4: Permission Denied
**Fix:**
```bash
chmod +x msm.sh
chmod +x install.sh
chmod +x core/*.py
```

---

## 🔧 Termux-Specific Commands

### Install Dependencies
```bash
# Core packages
pkg install openjdk-17 python wget curl git screen

# Python packages
pip install psutil requests flask tqdm colorama
```

### Storage Access
```bash
# Grant storage permissions
termux-setup-storage

# This creates ~/storage with:
# - downloads/
# - dcim/
# - shared/
```

### Keep Termux Awake
```bash
# Prevent Termux from sleeping
termux-wake-lock

# Release when done
termux-wake-unlock
```

---

## 📊 Recommended Settings for Android

### Low-End Device (2-3GB RAM)
```bash
Server Type: Paper
RAM: 1536-2048 MB
Cores: 1-2
Players: 5-10
View Distance: 6
```

### Mid-Range Device (4-6GB RAM)
```bash
Server Type: Paper/Purpur
RAM: 2048-3072 MB  
Cores: 2-3
Players: 10-20
View Distance: 8-10
```

### High-End Device (6GB+ RAM)
```bash
Server Type: Purpur
RAM: 4096+ MB
Cores: 3-4
Players: 20-50
View Distance: 10-12
```

---

## 🚀 Step-by-Step First Server

### 1. Start Manager
```bash
cd ~/minecraft-server-manager
bash msm.sh
```

### 2. Create Server
- Select `[1] Create New Server`
- Name: `myserver`
- Type: `2` (Paper)
- Version: `latest`
- RAM: `2048` (2GB)
- Cores: `2`
- Wait for download (2-5 minutes)

### 3. Start Server
- Select `[3] Start Server`
- Choose `myserver`
- Wait 30-60 seconds

### 4. Check Status
- Select `[12] Server Status`
- Verify server is RUNNING

### 5. Connect
- On same device: `localhost:25565`
- From other device: `<phone-ip>:25565`

Find your IP:
```bash
ifconfig wlan0 | grep inet
```

---

## 💡 Pro Tips for Termux

### 1. Battery & Performance
```bash
# Keep device plugged in
# Enable "Stay awake" in Developer Options
# Close other apps
# Use a cooling fan if possible
```

### 2. Network
```bash
# Use WiFi, not mobile data
# Static IP recommended
# Port forward 25565 on router
```

### 3. Stability
```bash
# Don't close Termux app
# Use wake lock
# Create swap file if low RAM:
dd if=/dev/zero of=/data/local/tmp/swapfile bs=1M count=1024
chmod 600 /data/local/tmp/swapfile
```

### 4. Monitoring
```bash
# Check resources
htop

# Monitor server
screen -r msm-myserver

# Detach from screen
# Press: Ctrl+A then D
```

---

## 🐛 Troubleshooting

### Server Crashes Immediately
```bash
# Check logs
cat ~/.msm/servers/myserver/logs/latest.log

# Common fixes:
# 1. Lower RAM allocation
# 2. Check Java version
# 3. Delete world and restart
# 4. Verify eula.txt accepted
```

### Can't Access Console
```bash
# List screen sessions
screen -list

# Reattach
screen -r msm-myserver

# If stuck, force detach
screen -D -r msm-myserver
```

### Out of Memory
```bash
# Check memory
free -m

# Free up space
apt clean
pkg clean

# Remove old backups
rm ~/.msm/backups/*/old_backup*.tar.gz
```

### Web Panel Not Accessible
```bash
# Check if running
ps aux | grep web_panel

# Check port
netstat -tulpn | grep 8080

# Restart
pkill -f web_panel
python core/web_panel.py
```

---

## 📁 Termux File Locations

```
~/minecraft-server-manager/    # Project files
~/.msm/                        # Data directory
~/.msm/servers/                # Server installations
~/.msm/backups/                # Server backups
~/.msm/plugins/                # Plugin cache
```

---

## 🔄 Updating

```bash
cd ~/minecraft-server-manager
git pull
bash install.sh
```

---

## ⚡ Quick Commands Reference

```bash
# Start manager
bash msm.sh

# Direct server control
python core/server_manager.py start <name>
python core/server_manager.py stop <name>

# Monitor resources
python core/resource_monitor.py

# Web panel
python core/web_panel.py

# Server console
screen -r msm-<name>

# List servers
ls ~/.msm/servers/
```

---

## 🆘 Need Help?

1. Check this README
2. View logs: `~/.msm/servers/<name>/logs/latest.log`
3. Run diagnostic: `bash termux-fix.sh`
4. Check Termux wiki: https://wiki.termux.com/

---

## ✅ Installation Checklist

- [ ] Termux installed from F-Droid
- [ ] Packages updated: `pkg update && pkg upgrade`
- [ ] Java installed: `pkg install openjdk-17`
- [ ] Python installed: `pkg install python`
- [ ] Storage permissions granted: `termux-setup-storage`
- [ ] Dependencies installed: `bash install.sh`
- [ ] Files executable: `chmod +x *.sh`
- [ ] Test run: `bash msm.sh`

---

**You're all set! Create your first server and start hosting! 🎮**

# Minecraft Server Manager - Quick Start Guide

## 🚀 Installation (5 minutes)

### 1. Install Termux
- Download from F-Droid: https://f-droid.org/packages/com.termux/
- Grant storage permissions

### 2. Setup
```bash
# Update Termux
pkg update -y && pkg upgrade -y

# Navigate to project
cd ~/minecraft-server-manager

# Install
./install.sh
```

### 3. Launch
```bash
./msm.sh
```

## 🎮 Create Your First Server (2 minutes)

1. Select `[1] Create New Server`
2. Enter name: `myserver`
3. Select type: `2` (Paper - Best performance)
4. Version: `latest`
5. RAM: `2048` (2GB)
6. Cores: `2`

Wait for download, then:

7. Select `[3] Start Server`
8. Select your server

**Done! Server is running!**

## 📱 Connect to Your Server

**From same device:**
```
localhost:25565
```

**From other devices (same WiFi):**
```
<your-phone-ip>:25565
```

Find your IP:
```bash
ifconfig | grep "inet "
```

## 🌐 Web Control Panel

```bash
# From main menu, select [10] Web Control Panel
# Then open browser to:
http://localhost:8080
```

## 📊 Monitor Performance

```bash
# From main menu, select [6] Resource Monitor
```

## 🔧 Console Access

```bash
# From main menu, select [5] Server Console
# Detach: Ctrl+A then D
```

## 💾 Backup Your Server

```bash
# From main menu, select [8] Backup Manager
# Then [1] Create Backup
```

## ⚡ Optimize Performance

```bash
# From main menu, select [9] Performance Tuning
# Then [6] Apply Performance Presets
# Select your device type
```

## 🎯 Recommended Settings by Device

### Low-End (2-3GB RAM)
- Server: Paper
- RAM: 2048 MB
- Cores: 2
- View Distance: 6
- Max Players: 10

### Mid-Range (4-6GB RAM)
- Server: Paper/Purpur
- RAM: 4096 MB
- Cores: 3
- View Distance: 10
- Max Players: 20

### High-End (6GB+ RAM)
- Server: Purpur
- RAM: 6144 MB
- Cores: 4
- View Distance: 12
- Max Players: 50+

## 🔥 Pro Tips

1. **Keep device plugged in** - Prevents battery drain
2. **Enable wake lock** - `termux-wake-lock`
3. **Close other apps** - Free more RAM
4. **Use Paper/Purpur** - 2x faster than Vanilla
5. **Regular backups** - Before installing plugins
6. **Monitor resources** - Keep CPU < 80%

## 🛠️ Troubleshooting

### Server won't start?
```bash
# Check Java
java -version

# Check RAM
free -m

# View logs
cat ~/.msm/servers/myserver/logs/latest.log
```

### Out of memory?
- Reduce RAM allocation in Performance Tuning
- Close other apps
- Lower view distance

### Can't connect?
- Check server is running (status shows RUNNING)
- Verify port: 25565
- Check firewall settings
- Try localhost:25565 first

## 📁 Important Locations

```bash
# Servers
~/.msm/servers/

# Backups
~/.msm/backups/

# Config
~/.msm/config.json

# Plugins
~/.msm/servers/<server-name>/plugins/

# Worlds
~/.msm/servers/<server-name>/world/
```

## 🎯 Common Commands

```bash
# Start manager
./msm.sh

# Web panel
python3 core/web_panel.py

# Monitor
python3 core/resource_monitor.py

# Status
python3 core/server_status.py

# Console
screen -r msm-<server-name>
```

## 🎉 Next Steps

1. ✅ Install essential plugins (EssentialsX, Vault, LuckPerms)
2. ✅ Configure server.properties
3. ✅ Set up automatic backups
4. ✅ Optimize JVM flags
5. ✅ Configure port forwarding for external access
6. ✅ Add players to whitelist

## 📚 Need More Help?

- Read full README.md
- Check server logs
- Visit Paper documentation: https://docs.papermc.io/
- Join Minecraft server communities

**Happy hosting! 🎮🚀**

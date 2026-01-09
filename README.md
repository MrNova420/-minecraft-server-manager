# 🎮 Minecraft Server Manager - Professional Edition

**The Ultimate Android Termux Minecraft Server Hosting Solution**

Transform your Android device into a high-performance, professional-grade Minecraft server hosting platform. Run any type of Minecraft server with full control over resources, plugins, mods, and configurations.

---

## ✨ Features

### 🚀 Server Types Supported
- **Vanilla** - Official Minecraft server
- **Paper** - Highly optimized (Recommended)
- **Spigot** - Plugin support
- **Purpur** - Best performance
- **Fabric** - Lightweight mods
- **Forge** - Heavy modpack support
- **NeoForge** - Latest mod loader
- **BungeeCord** - Server proxy
- **Velocity** - Modern proxy

### 💪 Advanced Resource Management
- **RAM Control** - Precise memory allocation (1GB - 8GB+)
- **CPU Core Assignment** - Dedicate specific cores to servers
- **Performance Monitoring** - Real-time CPU, RAM, disk usage
- **Automatic Optimization** - Smart JVM flags (Aikar's flags)
- **Resource Presets** - Low-end, mid-range, high-end configurations

### 🔧 Complete Server Control
- **Easy Creation** - Setup servers in minutes
- **Start/Stop/Restart** - Full lifecycle management
- **Console Access** - Direct server console via Screen
- **Multiple Servers** - Run several servers simultaneously
- **Port Management** - Automatic port assignment
- **Configuration Editor** - Edit server.properties

### 📦 Plugin & Mod Management
- **Browse Popular Plugins** - Curated plugin list
- **Search Functionality** - Find any plugin/mod
- **One-Click Install** - Download from URL
- **Manage Installed** - View and remove plugins
- **Multi-Platform** - Support for Spigot, CurseForge, Modrinth

### 💾 Backup System
- **Manual Backups** - Create backups anytime
- **Restore System** - Roll back to any backup
- **Compression** - Efficient tar.gz storage
- **Metadata Tracking** - Track backup dates and sizes
- **Multiple Versions** - Keep unlimited backups

### ⚡ Performance Tuning
- **JVM Optimization** - Multiple performance profiles
- **Server Properties** - Tuned configurations
- **View Distance Control** - Optimize rendering
- **Network Compression** - Reduce bandwidth usage
- **Automatic Presets** - Device-specific optimization

### 🌐 Web Control Panel
- **Beautiful Interface** - Modern, responsive design
- **Real-Time Stats** - Live resource monitoring
- **Remote Management** - Control from any browser
- **Server Cards** - Visual server overview
- **One-Click Actions** - Start, stop, restart servers

### 📊 Monitoring & Statistics
- **Live Dashboard** - Real-time system metrics
- **Per-Core CPU** - Individual core usage
- **Memory Tracking** - RAM usage per server
- **Network Stats** - Bandwidth monitoring
- **Server Status** - Comprehensive server info

---

## 📋 Requirements

### Minimum Requirements
- Android 7.0+
- 3GB RAM (2GB for server + 1GB for system)
- 2GB free storage
- Termux app
- Stable internet connection

### Recommended
- Android 10+
- 6GB+ RAM
- 4+ CPU cores
- 5GB+ free storage
- Power connection (prevents battery drain)

---

## 🚀 Installation

### Step 1: Install Termux
Download Termux from F-Droid (recommended):
```
https://f-droid.org/packages/com.termux/
```

### Step 2: Update Termux
```bash
pkg update -y && pkg upgrade -y
```

### Step 3: Download and Install
```bash
# Clone or download the repository
cd ~
git clone <repository-url> minecraft-server-manager

# Or download and extract
cd minecraft-server-manager

# Run installation
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Update system packages
- ✅ Install Java 17 & 21
- ✅ Install Python and dependencies
- ✅ Set up directory structure
- ✅ Configure permissions
- ✅ Create default config

### Step 4: Launch
```bash
cd ~/minecraft-server-manager
./msm.sh
```

---

## 📖 Usage Guide

### Creating Your First Server

1. **Launch the manager**
   ```bash
   ./msm.sh
   ```

2. **Select "Create New Server" [1]**

3. **Enter server details:**
   - Name: `my-server`
   - Type: `2` (Paper - Recommended)
   - Version: `latest` or specific like `1.20.4`
   - RAM: `2048` (2GB minimum)
   - Cores: `2` (recommended)

4. **Wait for download** - Server files will be downloaded automatically

5. **Start your server** - Select option [3] "Start Server"

### Accessing Server Console

```bash
# From main menu, select [5] "Server Console"
# Or directly:
screen -r msm-<server-name>

# Detach from console: Ctrl+A then D
```

### Managing Resources

**Adjust RAM:**
1. Select [9] "Performance Tuning"
2. Select [1] "Adjust RAM Allocation"
3. Choose server and enter new RAM amount

**Configure CPU:**
1. Select [9] "Performance Tuning"
2. Select [2] "Configure CPU Cores"
3. Choose server and set core count

### Installing Plugins

1. Select [7] "Plugin/Mod Manager"
2. Select [3] "Install Plugin from URL"
3. Choose server
4. Enter download URL
5. Plugin installs to server's plugins folder

### Creating Backups

1. Select [8] "Backup Manager"
2. Select [1] "Create Backup"
3. Choose server
4. Backup saved to `~/.msm/backups/`

### Web Control Panel

```bash
# From main menu, select [10] "Web Control Panel"
# Or directly:
python3 core/web_panel.py

# Access from browser:
http://localhost:8080
# Or from another device:
http://<your-device-ip>:8080
```

---

## 🎯 Performance Optimization

### For Low-End Devices (2-3GB RAM)
- Use Paper or Purpur server
- Allocate 2GB RAM maximum
- Set view-distance: 6-8
- Use 1-2 CPU cores
- Limit plugins (10-15 max)
- Reduce entity spawns

### For Mid-Range Devices (4-6GB RAM)
- Use Paper or Purpur
- Allocate 3-4GB RAM
- Set view-distance: 10
- Use 2-3 CPU cores
- Moderate plugins (20-30)
- Normal entity spawns

### For High-End Devices (6GB+ RAM)
- Any server type
- Allocate 4-6GB RAM
- Set view-distance: 12-16
- Use 4+ CPU cores
- Unlimited plugins
- No restrictions

### Optimization Tips

1. **Keep device cool** - Use a fan or cooling pad
2. **Stable power** - Keep plugged in
3. **Background apps** - Close unnecessary apps
4. **Network** - Use WiFi, not mobile data
5. **Storage** - Keep 2GB+ free space
6. **Wakelock** - Prevent device sleep

```bash
# Prevent Termux from sleeping
termux-wake-lock

# Release wakelock
termux-wake-unlock
```

---

## 🛠️ Advanced Configuration

### Custom JVM Flags

Edit `~/.msm/servers/<server-name>/jvm_flags.txt`

```bash
# Balanced (Default)
-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
# ... more flags

# Performance
-XX:MaxGCPauseMillis=100
-XX:G1NewSizePercent=40

# Memory Optimized
-XX:MaxGCPauseMillis=300
-XX:G1NewSizePercent=20
```

### Server Properties

Edit `~/.msm/servers/<server-name>/server.properties`

```properties
# Performance settings
view-distance=10
simulation-distance=8
network-compression-threshold=256

# Player limits
max-players=20

# World settings
spawn-protection=16
difficulty=normal
```

### Port Forwarding

To allow external connections:

1. **Find your local IP:**
   ```bash
   ifconfig
   # Look for wlan0 inet address
   ```

2. **Configure router:**
   - Log into router admin panel
   - Find "Port Forwarding" section
   - Forward port 25565 to your device IP
   - Protocol: TCP

3. **Share your public IP:**
   ```bash
   curl ifconfig.me
   ```

---

## 📁 Directory Structure

```
~/.msm/
├── servers/           # All server installations
│   ├── server1/
│   │   ├── server.jar
│   │   ├── start.sh
│   │   ├── jvm_flags.txt
│   │   ├── msm_config.json
│   │   ├── server.properties
│   │   ├── plugins/
│   │   └── world/
│   └── server2/
├── backups/           # Server backups
│   ├── server1/
│   │   ├── server1_20260109_120000.tar.gz
│   │   └── server1_20260109_120000.json
├── plugins/           # Plugin cache
├── mods/              # Mod cache
└── config.json        # Global configuration
```

---

## 🔍 Troubleshooting

### Server Won't Start

**Check Java installation:**
```bash
java -version
```

**Check RAM availability:**
```bash
free -m
```

**View server logs:**
```bash
cat ~/.msm/servers/<server-name>/logs/latest.log
```

### Out of Memory

**Reduce RAM allocation:**
```bash
# Edit server config
nano ~/.msm/servers/<server-name>/msm_config.json
# Change "ram" value to lower amount
```

**Close other apps:**
```bash
# Check memory usage
htop
```

### Server Crash on Join

**Lower view distance:**
```bash
nano ~/.msm/servers/<server-name>/server.properties
# Set view-distance=6
```

**Reduce entities:**
Install plugins like ClearLag to manage entities

### Can't Access Console

**List screen sessions:**
```bash
screen -list
```

**Reattach to session:**
```bash
screen -r msm-<server-name>
```

### Web Panel Not Loading

**Check if running:**
```bash
ps aux | grep web_panel
```

**Check port:**
```bash
netstat -tulpn | grep 8080
```

**Restart web panel:**
```bash
pkill -f web_panel
python3 ~/minecraft-server-manager/core/web_panel.py
```

---

## 🤝 Support

### Getting Help

1. Check this README
2. View server logs
3. Check Termux logs
4. Search for error messages online
5. Ask in Minecraft server communities

### Common Resources

- **Paper Documentation:** https://docs.papermc.io/
- **Spigot Wiki:** https://www.spigotmc.org/wiki/
- **Fabric Wiki:** https://fabricmc.net/wiki/
- **Termux Wiki:** https://wiki.termux.com/

---

## 📝 Tips & Best Practices

### Server Management
✅ **Regular backups** - Backup before major changes  
✅ **Update plugins** - Keep plugins current  
✅ **Monitor resources** - Check CPU/RAM regularly  
✅ **Optimize worlds** - Use pregeneration  
✅ **Clean logs** - Delete old log files  

### Security
✅ **Change default port** - Use non-standard ports  
✅ **Whitelist players** - For private servers  
✅ **Use permissions** - Install LuckPerms  
✅ **Regular updates** - Keep server software updated  
✅ **Backup often** - Protect against data loss  

### Performance
✅ **Use Paper/Purpur** - Better than Vanilla  
✅ **Limit view distance** - Huge performance impact  
✅ **Control entities** - Mob spawners, farms  
✅ **Pregen worlds** - Avoid runtime generation  
✅ **Monitor TPS** - Keep above 19.5  

---

## 🎉 Features Coming Soon

- 🔄 **Auto-restart on crash**
- ⏰ **Scheduled backups**
- ☁️ **Cloud backup integration**
- 📊 **Advanced statistics**
- 🔔 **Discord notifications**
- 🌍 **Multi-world management**
- 👥 **Player management**
- 📈 **Performance graphs**

---

## 📜 License

This project is open-source and available for personal use. Feel free to modify and share!

---

## 🌟 Credits

- **Paper Project** - Optimized server software
- **Aikar** - JVM optimization flags
- **Termux Team** - Android Linux environment
- **Minecraft Community** - Endless support

---

## 🚀 Quick Reference

### Common Commands

```bash
# Start server manager
./msm.sh

# Direct server control
python3 core/server_manager.py start <server-name>
python3 core/server_manager.py stop <server-name>
python3 core/server_manager.py restart <server-name>

# Access console
screen -r msm-<server-name>

# Monitor resources
python3 core/resource_monitor.py

# Web panel
python3 core/web_panel.py

# Server status
python3 core/server_status.py

# Backups
python3 core/backup_manager.py

# Settings
python3 core/settings.py
```

### Default Ports
- Minecraft: `25565` (auto-increments for multiple servers)
- Web Panel: `8080`

### Default Locations
- Servers: `~/.msm/servers/`
- Backups: `~/.msm/backups/`
- Config: `~/.msm/config.json`

---

**Made with ❤️ for the Minecraft community**

**Host amazing servers from your Android device! 🎮📱**

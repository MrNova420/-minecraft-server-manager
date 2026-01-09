# 🚀 COMPLETE QUICK START GUIDE

## ⚡ FASTEST WAY TO GET STARTED

### 1. Run System Test (FIRST!)
```bash
cd minecraft-server-manager
bash test-all.sh
```

**This checks:**
- ✅ All files present
- ✅ Dependencies installed
- ✅ Python modules working
- ✅ Enough RAM/storage
- ✅ Everything ready

If you see errors, run: `bash install.sh`

---

## 🎮 CREATE YOUR FIRST SERVER

### Option A: Java + Bedrock Together (CROSSPLAY) ⭐ RECOMMENDED
```bash
bash msm.sh
```

1. Select **[1] Create New Server**
2. Name: `survival`
3. Select **[11] Paper+Geyser (Crossplay)**
4. Version: `latest` (press Enter)
5. RAM: `3072` (3GB recommended)
6. Cores: `2` (press Enter)

Wait 2-3 minutes for download...

### Option B: Java Only (PC Players)
```bash
bash msm.sh
```

1. Select **[1] Create New Server**
2. Name: `survival`
3. Select **[2] Paper** (optimized)
4. Version: `latest`
5. RAM: `2048` (2GB)
6. Cores: `2`

### Option C: Bedrock Only (Mobile/Console)
```bash
bash msm.sh
```

1. Select **[1] Create New Server**
2. Name: `pocket`
3. Select **[10] Bedrock**
4. RAM: `2048`
5. Cores: `2`

---

## ▶️ START THE SERVER

```bash
bash msm.sh
```

1. Select **[3] Start Server**
2. Choose your server (e.g., `survival`)
3. Wait 30-60 seconds for full startup

**Check if running:**
```bash
screen -list | grep msm
```
Should see: `msm-survival`

---

## 📱 CONNECT TO SERVER

### Get Your IP:
```bash
bash msm.sh
# Select [13] Connection Info
```

OR manually:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Example output: `192.168.1.50`

### Connect Players:

**Java Edition (PC/Mac):**
- Open Minecraft Java Edition
- Multiplayer → Add Server
- Address: `192.168.1.50:25565`
- Save and join!

**Bedrock Edition (Mobile/Console):**
- Open Minecraft PE/Bedrock
- Play → Servers → Add Server
- Server Name: `My Server`
- Server Address: `192.168.1.50`
- Port: `19132`
- Save and join!

**IMPORTANT:** Both devices must be on **SAME WiFi network!**

---

## 🔌 ADD PLUGINS/MODS

### Easy Way (NEW!):
```bash
bash msm.sh
# Select [15] Easy Plugin/Mod Installer
```

Choose your server, then:
- **[1]** Install from URL
- **[2]** Install from file
- **[3]** Install popular plugins/mods
- **[4]** List installed
- **[5]** Remove a plugin/mod

### Popular Plugins:
The installer includes:
- EssentialsX - Essential commands
- LuckPerms - Permissions
- WorldEdit - World editing
- WorldGuard - Protection
- CoreProtect - Anti-grief
- Dynmap - Web map
- And more!

### Manual Way:
```bash
# For plugin servers (Paper, Spigot, Purpur)
cd ~/.msm/servers/YOUR-SERVER/plugins/
wget https://url-to-plugin.jar

# For mod servers (Fabric, Forge)
cd ~/.msm/servers/YOUR-SERVER/mods/
wget https://url-to-mod.jar
```

**Then restart server:**
```bash
bash msm.sh
# [4] Stop Server
# [3] Start Server
```

---

## 🛠️ COMMON TASKS

### View Server Console:
```bash
bash msm.sh
# [5] Server Console
```
Press `Ctrl+A` then `D` to detach

### Stop Server:
```bash
bash msm.sh
# [4] Stop Server
```

### Check Server Status:
```bash
bash msm.sh
# [12] Server Status
```

### Monitor Resources:
```bash
bash msm.sh
# [6] Resource Monitor
```

### Backup Server:
```bash
bash msm.sh
# [8] Backup Manager
```

### Performance Tuning:
```bash
bash msm.sh
# [9] Performance Tuning
```

---

## 🩺 TROUBLESHOOTING

### Can't Connect?
```bash
bash msm.sh
# [14] Diagnose Connection Issues
```

This will check EVERYTHING and tell you what's wrong!

### Server Won't Start?
```bash
# Check logs
tail -50 ~/.msm/servers/YOUR-SERVER/logs/latest.log

# Check if Java is running
ps aux | grep java

# Test system
bash test-all.sh
```

### Not Enough RAM?
```bash
# Check free RAM
free -m

# Lower server RAM allocation
bash msm.sh
# [9] Performance Tuning → Lower RAM
```

### Plugin/Mod Not Working?
```bash
# Check if loaded
tail -100 ~/.msm/servers/YOUR-SERVER/logs/latest.log | grep -i "plugin\|mod"

# List installed
bash add-plugin.sh
# [4] List installed plugins/mods
```

---

## 📚 FULL DOCUMENTATION

### All Server Types Explained:
```bash
cat SERVER-TYPES-GUIDE.md
```

### Connection Issues:
```bash
cat CONNECTION-FIX.md
```

### Bedrock/Crossplay Setup:
```bash
cat BEDROCK-CROSSPLAY.md
```

### Complete Features:
```bash
cat README.md
```

---

## ⚙️ CONFIGURATION

### Server Settings:
```bash
nano ~/.msm/servers/YOUR-SERVER/server.properties
```

Key settings:
- `server-port=25565` - Port number
- `max-players=20` - Max players
- `difficulty=normal` - Difficulty
- `gamemode=survival` - Default gamemode
- `online-mode=true` - Authentication (set false for offline)

### Whitelist Players:
```bash
# Enter console
screen -r msm-YOUR-SERVER

# Add player
whitelist add PlayerName
whitelist on

# Exit console (Ctrl+A then D)
```

### Op Players (Admin):
```bash
screen -r msm-YOUR-SERVER
op PlayerName
```

---

## 🌐 WEB CONTROL PANEL

```bash
bash msm.sh
# [10] Web Control Panel
```

Access from any device on same WiFi:
```
http://192.168.1.50:8080
```

Features:
- Start/stop servers
- View status
- Monitor resources
- Real-time stats

---

## 🔄 ADVANCED: Multiple Servers

You can run multiple servers at once!

```bash
bash msm.sh
# [1] Create New Server → Create server "survival"
# [1] Create New Server → Create server "creative"
# [1] Create New Server → Create server "modded"

# Start all
# [3] Start Server → survival
# [3] Start Server → creative
# [3] Start Server → creative
```

Each uses different ports automatically:
- survival: 25565
- creative: 25566
- modded: 25567

---

## 📊 RECOMMENDED SPECS

### For 5-10 Players:
- **Java-only:** 2-3GB RAM
- **Crossplay:** 3-4GB RAM
- **Bedrock:** 1-2GB RAM
- **Storage:** 2-5GB free

### For 10-20 Players:
- **Java-only:** 3-4GB RAM
- **Crossplay:** 4-5GB RAM
- **Bedrock:** 2-3GB RAM
- **Storage:** 5-10GB free

### For 20+ Players:
- **Java-only:** 4-6GB RAM
- **Crossplay:** 5-7GB RAM
- **Bedrock:** 3-4GB RAM
- **Storage:** 10GB+ free

---

## 🎯 QUICK REFERENCE

### Essential Commands:
```bash
# Main menu
bash msm.sh

# Quick plugin install
bash add-plugin.sh

# Diagnose problems
bash diagnose.sh

# Test system
bash test-all.sh

# Connection info
bash server-info.sh

# View server logs
tail -f ~/.msm/servers/YOUR-SERVER/logs/latest.log

# List running servers
screen -list | grep msm

# Check Java processes
ps aux | grep java
```

### Important Directories:
```
~/.msm/                     Main directory
~/.msm/servers/             All servers
~/.msm/servers/NAME/        Specific server
~/.msm/servers/NAME/plugins/ Plugin folder
~/.msm/servers/NAME/mods/   Mod folder
~/.msm/backups/             Backups
```

---

## ✅ COMPLETE CHECKLIST

Before asking for help, verify:

- [ ] Ran `bash test-all.sh` - all green ✓
- [ ] Server shows [RUNNING] in menu
- [ ] Waited 30-60 seconds after starting
- [ ] Both devices on SAME WiFi
- [ ] Used correct IP address
- [ ] Used correct port (25565 Java, 19132 Bedrock)
- [ ] Ran `bash diagnose.sh` for issues
- [ ] Checked server logs for errors
- [ ] Have 2GB+ free RAM

---

## 🆘 STILL STUCK?

### Run Full Diagnostic:
```bash
bash test-all.sh && bash diagnose.sh
```

### Check Everything:
```bash
# System status
bash test-all.sh

# Connection diagnostic  
bash diagnose.sh

# Server logs
tail -100 ~/.msm/servers/YOUR-SERVER/logs/latest.log

# Network status
ifconfig
netstat -tulpn | grep -E "25565|19132"

# Server properties
cat ~/.msm/servers/YOUR-SERVER/server.properties | grep -E "server-ip|port|online-mode"
```

### Share This Info:
When asking for help, provide:
1. Output of `bash test-all.sh`
2. Output of `bash diagnose.sh`
3. Last 50 lines of server log
4. Your server type and settings

---

## 🎉 YOU'RE READY!

You now know how to:
- ✅ Create any type of server
- ✅ Start and stop servers
- ✅ Connect players
- ✅ Install plugins/mods
- ✅ Troubleshoot issues
- ✅ Configure settings
- ✅ Monitor performance

**Just run:** `bash msm.sh`

**Have fun! 🎮**

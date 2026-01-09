# 🚀 SERVER STARTUP TROUBLESHOOTING GUIDE

## ✅ Critical Fixes Applied

### Fixed Issues:
1. **Removed `taskset`** - Not available on Android/Termux
2. **Fixed `--nogui` flag** - Changed to `nogui` (no dashes)
3. **Simplified JVM flags** - Removed flags that don't work on Android
4. **Better error handling** - Fallback for missing files

---

## 📋 Pre-Flight Checklist

Before creating your first server, verify:

```bash
# 1. Java installed and working
java -version
# Should show: openjdk version "17..." or higher

# 2. Screen installed
screen -version
# Should show: Screen version 4.x.x

# 3. Python working
python --version
# Should show: Python 3.x.x

# 4. Sufficient RAM
free -m
# Should show at least 2GB free

# 5. Sufficient storage
df -h ~
# Should show at least 2GB free
```

---

## 🎮 Creating Your First Server

### Step 1: Start Manager
```bash
cd ~/minecraft-server-manager
bash msm.sh
```

### Step 2: Create Server
```
Select: [1] Create New Server
Name: testserver
Type: 2 (Paper - RECOMMENDED for Android)
Version: latest (or specific like 1.20.4)
RAM: 1536 (for testing) or 2048 (for real use)
Cores: 2 (doesn't affect much on Android)
```

**Wait 2-5 minutes** - Downloads ~50MB server jar

### Step 3: Verify Creation
```bash
ls ~/.msm/servers/testserver/
# Should see: server.jar, start.sh, eula.txt, etc.
```

### Step 4: Check Start Script
```bash
cat ~/.msm/servers/testserver/start.sh
# Should NOT contain "taskset"
# Should show: java ... -jar server.jar nogui
```

### Step 5: Start Server
```
Select: [3] Start Server
Choose: testserver
Wait: 30-60 seconds for startup
```

### Step 6: Verify Running
```bash
screen -list
# Should show: msm-testserver

# Check if Java is running
ps aux | grep java
# Should show java process
```

### Step 7: Access Console
```
Select: [5] Server Console
Choose: testserver

# In console, type:
help
list

# To exit console without stopping server:
# Press: Ctrl+A then D
```

---

## 🐛 Common Startup Problems

### Problem: "Command not found: taskset"
**Status:** FIXED in latest version
**Solution:** Update your files (git pull)

### Problem: Server jar not found
**Symptoms:** Error immediately after start
**Fix:**
```bash
cd ~/.msm/servers/<yourserver>
ls -lh server.jar
# Should exist and be ~50MB

# If missing, recreate server or download manually
```

### Problem: Out of memory
**Symptoms:** Server crashes after 10-30 seconds
**Fix:**
```bash
# Check available RAM
free -m

# Lower RAM allocation:
# Edit server config
cd ~/.msm/servers/<yourserver>
nano msm_config.json
# Change "ram": 2048 to "ram": 1536

# Or use performance tuner in main menu
```

### Problem: Screen session disappears
**Symptoms:** Screen session vanishes after start
**Cause:** Server crashed, check logs
**Fix:**
```bash
# View logs
cat ~/.msm/servers/<yourserver>/logs/latest.log

# Common issues in logs:
# - Java version error: Install openjdk-17
# - Port in use: Change port in server.properties
# - EULA: Should auto-accept, check eula.txt
```

### Problem: "Invalid or corrupt jarfile"
**Symptoms:** Error about jar file
**Fix:**
```bash
# Redownload server jar
cd ~/.msm/servers/<yourserver>
rm server.jar

# Then recreate server or download manually:
# For Paper 1.20.4:
wget https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar -O server.jar
```

### Problem: Can't connect to server
**Symptoms:** Minecraft says "Can't connect"
**Checks:**
```bash
# 1. Is server running?
screen -list

# 2. Is Java running?
ps aux | grep java

# 3. Check console for "Done"
screen -r msm-<yourserver>
# Look for: [Server thread/INFO]: Done (10.5s)!

# 4. Verify port
cat ~/.msm/servers/<yourserver>/server.properties | grep server-port

# 5. In Minecraft, connect to:
# Same device: localhost:25565
# Other device: <your-phone-ip>:25565
```

---

## 📊 Expected Startup Times

### Server Creation (First time)
- Download time: 2-5 minutes (depends on internet)
- Setup: 5-10 seconds
- Total: ~5 minutes

### Server Startup (Each time)
- Low RAM (1-2GB): 45-90 seconds
- Medium RAM (2-4GB): 30-60 seconds
- High RAM (4GB+): 20-40 seconds

### Signs Server is Starting:
```bash
# In console (screen -r msm-<name>):
[Server thread/INFO]: Starting minecraft server version X.X.X
[Server thread/INFO]: Loading properties
[Server thread/INFO]: Preparing level "world"
[Server thread/INFO]: Preparing spawn area: XX%
[Server thread/INFO]: Done (XX.XXs)! For help, type "help"
```

When you see **"Done"** - server is ready!

---

## 💡 Optimization Tips for Android

### 1. Use Paper or Purpur
These are 2-3x faster than Vanilla on Android

### 2. Lower View Distance
```properties
# In server.properties:
view-distance=6    # Low-end
view-distance=8    # Mid-range
view-distance=10   # High-end
```

### 3. Reduce RAM if Crashing
```bash
# Performance Tuner > Adjust RAM
# Try: 1536 MB, 1792 MB, 2048 MB
# Find sweet spot for your device
```

### 4. Keep Device Cool
- Use external fan
- Don't cover device
- Take breaks between sessions

### 5. Minimize Background Apps
```bash
# Before starting server:
# Close ALL other apps
# Disable auto-sync
# Turn off notifications
```

### 6. Use WiFi, Not Data
Mobile data causes lag and uses tons of bandwidth

### 7. Keep Device Plugged In
Server uses lots of battery

### 8. Enable Wake Lock
```bash
termux-wake-lock
# Prevents Termux from sleeping
```

---

## 🔍 Debug Commands

```bash
# Test if everything works
bash test-server-start.sh

# Check Java
java -version

# Check available RAM
free -m

# Check storage
df -h ~

# List servers
ls -lh ~/.msm/servers/

# Check server config
cat ~/.msm/servers/<name>/msm_config.json

# View start script
cat ~/.msm/servers/<name>/start.sh

# View server logs
tail -f ~/.msm/servers/<name>/logs/latest.log

# List screen sessions
screen -list

# Attach to server console
screen -r msm-<name>

# Kill stuck server
screen -S msm-<name> -X quit
pkill -f "java.*<name>"

# Test screen
screen -dmS test echo "works"
screen -list
screen -S test -X quit
```

---

## ✅ Success Indicators

Your server is working if:
- ✓ Screen session exists: `screen -list`
- ✓ Java process running: `ps aux | grep java`
- ✓ Console shows "Done": `screen -r msm-<name>`
- ✓ Can connect in Minecraft: `localhost:25565`
- ✓ Port is listening: `netstat -tlnp | grep 25565`

---

## 🆘 Still Not Working?

1. Run diagnostic: `bash test-server-start.sh`
2. Check logs: `cat ~/.msm/servers/<name>/logs/latest.log`
3. Verify Java: `java -version`
4. Check RAM: `free -m` (need at least 2GB free)
5. Read TERMUX-README.md
6. Start with Paper server, 1536 MB RAM, latest version

---

## 📞 Quick Reference

**Start manager:** `bash msm.sh`
**Test startup:** `bash test-server-start.sh`
**View console:** `screen -r msm-<name>`
**Exit console:** `Ctrl+A then D`
**Check logs:** `cat ~/.msm/servers/<name>/logs/latest.log`
**Find IP:** `ifconfig wlan0 | grep inet`

---

**Updated for Android/Termux - Servers WILL start now!** ✅

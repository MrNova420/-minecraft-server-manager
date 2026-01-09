# 🎮 BEDROCK & CROSSPLAY UPDATE

## ✨ NEW SERVER TYPES ADDED!

### Option 10: Bedrock Server (Minecraft PE/Mobile)
- **Native Bedrock server** for Pocket Edition players
- Runs on **port 19132** (UDP)
- Works with iOS, Android, Windows 10/11, Xbox, PlayStation, Nintendo Switch
- No Java required on client side!

### Option 11: Paper + Geyser (CROSSPLAY)
- **Java + Bedrock players on the SAME server!**
- Java players connect on port **25565**
- Bedrock players connect on port **19132**
- Includes Floodgate for offline Bedrock authentication
- Best of both worlds!

## 🚀 QUICK START

### Create a Bedrock Server:
```bash
bash msm.sh
# Select [1] Create New Server
# Select [10] Bedrock (Minecraft PE/Mobile)
# Configure RAM, etc.
```

### Create a Crossplay Server:
```bash
bash msm.sh
# Select [1] Create New Server
# Select [11] Paper+Geyser (CROSSPLAY)
# Configure RAM, etc.
```

## 🔌 CONNECTION PORTS

| Server Type | Java Port | Bedrock Port |
|-------------|-----------|--------------|
| Java Only   | 25565     | N/A          |
| Bedrock Only| N/A       | 19132        |
| Crossplay   | 25565     | 19132        |

## 🛠️ CONNECTION FIXES

### CRITICAL FIX #1: Server IP Binding
All servers now automatically set:
```properties
server-ip=0.0.0.0
```
This allows connections from ANY device on your network!

### CRITICAL FIX #2: Query Enabled
```properties
enable-query=true
query.port=25565
```
This lets Minecraft clients see your server status!

### CRITICAL FIX #3: MOTD Added
```properties
motd=Termux Minecraft Server - <your-server-name>
```
Players can see your server name in the server list!

## 🩺 NEW DIAGNOSTIC TOOL

### Option 14: Diagnose Connection Issues
```bash
bash msm.sh
# Select [14] Diagnose Connection Issues
```

This tool checks:
- ✅ Is server running?
- ✅ Is Java process active?
- ✅ Are ports listening?
- ✅ Server configuration correct?
- ✅ Your IP addresses
- ✅ Connection test results
- ✅ Recent error logs

## 📖 TROUBLESHOOTING GUIDE

Full troubleshooting documentation:
```bash
cat CONNECTION-FIX.md
```

Or run diagnostic:
```bash
bash diagnose.sh
```

## 🎯 COMMON ISSUES SOLVED

### ❌ "Can't connect to server"
**SOLUTION:** 
1. Wait 30-60 seconds for server to fully start
2. Check you're on the SAME WiFi network
3. Use local IP (192.168.x.x) not external
4. Run: `bash diagnose.sh`

### ❌ "Connection timeout"
**SOLUTION:**
```bash
# Check if server is actually running
screen -list | grep msm

# Check network ports
netstat -tulpn | grep 25565

# Verify server.properties
cat ~/.msm/servers/YOUR-SERVER/server.properties | grep server-ip
# Must be: server-ip=0.0.0.0
```

### ❌ "Failed to verify username"
**SOLUTION:**
Edit `server.properties`:
```properties
online-mode=false
```
Then restart server.

### ❌ "Bedrock players can't join crossplay server"
**SOLUTION:**
1. Wait for Geyser plugin to load (check logs)
2. Bedrock players use port **19132** not 25565
3. Check Geyser config:
```bash
cat ~/.msm/servers/YOUR-SERVER/plugins/Geyser-Spigot/config.yml
```

## 🌐 HOW TO CONNECT

### From Same Device (Testing):
```
localhost:25565
```

### From Other Device on Same WiFi:
```bash
# Get your IP first
ifconfig | grep "inet " | grep -v 127.0.0.1
# Example output: 192.168.1.50

# Then connect to:
192.168.1.50:25565  (Java)
192.168.1.50:19132  (Bedrock)
```

### From Internet (Advanced):
1. Port forward on router: 25565 → Your Android IP
2. Use public IP: `curl ifconfig.me`
3. Or use tunnel service like ngrok/Playit.gg

## 📱 BEDROCK SPECIFIC NOTES

### Server Files Location:
```
~/.msm/servers/YOUR-SERVER/
├── bedrock_server (binary)
├── server.properties
├── permissions.json
├── allowlist.json (whitelist)
└── worlds/
```

### Important Files:
- **allowlist.json** - Whitelist players
- **permissions.json** - Op players
- **server.properties** - Configuration

### Bedrock Commands:
```bash
# Connect to console
screen -r msm-YOUR-SERVER

# Common commands (in console)
allowlist add PlayerName
allowlist reload
op PlayerName
save hold
save resume
```

## 🔧 MANUAL FIXES

### Fix existing server to allow connections:
```bash
# Edit server.properties
nano ~/.msm/servers/YOUR-SERVER/server.properties

# Change or add:
server-ip=0.0.0.0
enable-query=true
query.port=25565

# Restart server
bash msm.sh → Stop Server → Start Server
```

### Add crossplay to existing Java server:
```bash
# Download Geyser
cd ~/.msm/servers/YOUR-SERVER/plugins
wget https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot -O Geyser-Spigot.jar

# Download Floodgate
wget https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot -O Floodgate-Spigot.jar

# Restart server
bash msm.sh → Stop Server → Start Server
```

## 📊 PERFORMANCE TIPS

### Bedrock Server:
- RAM: 1-2GB usually enough
- Lighter than Java servers
- Better for mobile devices

### Crossplay Server:
- RAM: 3-4GB recommended
- Geyser adds ~200MB overhead
- More players = more RAM

### View RAM usage:
```bash
ps aux | grep -E "java|bedrock" | grep -v grep
```

## ✅ VERIFICATION CHECKLIST

Before reporting issues, verify:
- [ ] Server shows [RUNNING] in `bash msm.sh`
- [ ] Port is listening: `netstat -tulpn | grep 25565`
- [ ] Server log shows "Done": `tail ~/.msm/servers/YOUR-SERVER/logs/latest.log`
- [ ] server-ip=0.0.0.0 in server.properties
- [ ] Both devices on SAME WiFi network
- [ ] Used correct port (25565 Java, 19132 Bedrock)
- [ ] Waited 30-60 seconds after starting server

## 🆘 GET HELP

If still having issues:
1. Run diagnostic: `bash diagnose.sh`
2. Check logs: `cat ~/.msm/servers/YOUR-SERVER/logs/latest.log`
3. View server properties: `cat ~/.msm/servers/YOUR-SERVER/server.properties`
4. Check network: `ifconfig` and `netstat -tulpn`

Share this output for better help!

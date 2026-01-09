# 🔧 CONNECTION TROUBLESHOOTING GUIDE

## WHY CAN'T PLAYERS CONNECT?

### ✅ CHECKLIST - Fix These First:

1. **Is the server actually running?**
   ```bash
   screen -list | grep msm
   ```
   Should see: `msm-yourserver`

2. **Is Java server process running?**
   ```bash
   ps aux | grep java | grep -v grep
   ```
   Should see a java process

3. **Check server logs for errors:**
   ```bash
   tail -50 ~/.msm/servers/YOUR-SERVER-NAME/logs/latest.log
   ```

4. **Test if port is listening:**
   ```bash
   netstat -tulpn | grep 25565
   ```
   OR
   ```bash
   ss -tulpn | grep 25565
   ```

## 🔥 CRITICAL FIXES FOR ANDROID/TERMUX

### Issue 1: Server binding to wrong IP
**FIX:** server.properties must have:
```properties
server-ip=0.0.0.0
```
NOT `127.0.0.1` or blank!

### Issue 2: Firewall / Network issues
Android may block incoming connections. You need:

1. **Same WiFi network** - Both device running server and player must be on SAME WiFi
2. **Use local IP** - Connect to `192.168.x.x:25565` NOT external IP
3. **Test with localhost first:**
   ```bash
   telnet localhost 25565
   ```

### Issue 3: Port already in use
```bash
# Check what's using the port
lsof -i :25565
# OR
netstat -tulpn | grep 25565
```

### Issue 4: Online mode vs Offline mode
If players get "Failed to verify username":
- Edit `server.properties`
- Set `online-mode=false` (allows cracked/offline players)

### Issue 5: Server not fully started
Server takes 30-60 seconds to start. Wait for:
```
[Server thread/INFO]: Done (15.234s)! For help, type "help"
```

## 📱 BEDROCK (Pocket Edition) SPECIFIC

### Bedrock Server Port
- **Java Edition:** Port 25565 (TCP)
- **Bedrock Edition:** Port 19132 (UDP)

### Bedrock Connection Issues:
1. Check `server.properties` in bedrock folder:
   ```properties
   server-port=19132
   server-portv6=19133
   ```

2. Bedrock uses UDP not TCP:
   ```bash
   netstat -unp | grep 19132
   ```

## 🌐 CROSSPLAY (Paper + Geyser)

### How Crossplay Works:
- **Java players:** Connect to `IP:25565`
- **Bedrock players:** Connect to `IP:19132`

### Geyser Config Location:
```bash
~/.msm/servers/YOUR-SERVER/plugins/Geyser-Spigot/config.yml
```

### Fix Geyser not working:
1. Check Geyser started:
   ```bash
   tail -100 ~/.msm/servers/YOUR-SERVER/logs/latest.log | grep -i geyser
   ```

2. Verify Geyser port:
   ```bash
   cat ~/.msm/servers/YOUR-SERVER/plugins/Geyser-Spigot/config.yml | grep port
   ```

3. Bedrock players need Floodgate for offline auth

## 🛠️ MANUAL CONNECTION TEST

### Test from Android device itself:
```bash
# Install netcat
pkg install netcat-openbsd

# Test connection
nc -zv localhost 25565
# Should say: Connection succeeded

# Or telnet
telnet localhost 25565
# Should connect and show gibberish (Minecraft protocol)
```

### Test from another device on same WiFi:
1. Get server device IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   Example: `192.168.1.50`

2. From other device:
   - Open Minecraft
   - Add Server
   - Address: `192.168.1.50:25565`
   - Try to connect

## 🔍 DEBUG COMMANDS

### View real-time server console:
```bash
screen -r msm-YOUR-SERVER-NAME
# Press Ctrl+A then D to detach
```

### Check what IPs server is listening on:
```bash
netstat -tulpn | grep java
```
Should show: `0.0.0.0:25565` NOT `127.0.0.1:25565`

### Force server to listen on all IPs:
Edit `server.properties`:
```properties
server-ip=0.0.0.0
query.port=25565
enable-query=true
enable-status=true
```

Restart server:
```bash
bash msm.sh
# Option 3 (Stop Server)
# Option 2 (Start Server)
```

## 🌍 INTERNET/EXTERNAL ACCESS

### Accessing from outside your network:
1. **Find your PUBLIC IP:**
   ```bash
   curl ifconfig.me
   ```

2. **Port forward on your router:**
   - Log into router admin (usually 192.168.1.1)
   - Find "Port Forwarding" or "Virtual Server"
   - Forward external port 25565 → internal IP (your Android device) port 25565
   - Protocol: TCP

3. **Dynamic DNS (if IP changes):**
   Use service like No-IP, DuckDNS for free domain

### Mobile Hotspot Issues:
⚠️ **Most mobile carriers block port forwarding**
- AT&T, Verizon, T-Mobile usually block inbound connections
- Use services like ngrok or Playit.gg for tunneling

## 📊 QUICK DIAGNOSTIC SCRIPT

Save as `check-connection.sh`:
```bash
#!/data/data/com.termux/files/usr/bin/bash

echo "=== Server Connection Diagnostic ==="
echo ""

# Check if server is running
echo "1. Server Process:"
if screen -list | grep -q msm-; then
    echo "   ✓ Screen session found"
    screen -list | grep msm-
else
    echo "   ✗ No server running!"
fi

echo ""
echo "2. Java Process:"
if ps aux | grep -q "[j]ava.*server.jar"; then
    echo "   ✓ Java server running"
else
    echo "   ✗ No Java process found!"
fi

echo ""
echo "3. Listening Ports:"
netstat -tulpn 2>/dev/null | grep -E ":(25565|19132)" || echo "   ✗ No ports listening!"

echo ""
echo "4. Server IP addresses:"
ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1

echo ""
echo "5. Test localhost connection:"
timeout 2 bash -c "</dev/tcp/localhost/25565" 2>/dev/null && echo "   ✓ Port 25565 responding!" || echo "   ✗ Port 25565 not accessible"

echo ""
echo "Done!"
```

Run it:
```bash
chmod +x check-connection.sh
bash check-connection.sh
```

## 🎯 COMMON ERROR MESSAGES

### "Connection timed out"
- Server not running, wrong IP, or firewall blocking

### "Connection refused"
- Server not started yet, or wrong port

### "Failed to verify username"
- Set `online-mode=false` in server.properties

### "Outdated client/server"
- Version mismatch - client and server must match

### "Invalid session"
- Authentication issue - try restarting Minecraft client

## ✅ VERIFIED WORKING SETUP

```bash
# 1. Create Paper+Geyser server
bash msm.sh → Option 1 → Option 11

# 2. Wait for server to fully start (2-3 minutes)

# 3. Get your IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# 4. Connect:
#    - Java players: IP:25565
#    - Bedrock players: IP:19132
```

## 📞 Still Not Working?

Check these files and share output:
```bash
# Server config
cat ~/.msm/servers/YOUR-SERVER/server.properties

# Latest log
tail -100 ~/.msm/servers/YOUR-SERVER/logs/latest.log

# Network status
netstat -tulpn | grep java

# Your IP addresses
ifconfig
```

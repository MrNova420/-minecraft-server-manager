# 🌐 COMPLETE CROSSPLAY SERVER GUIDE

## 📱 ALL SERVER TYPES EXPLAINED

### JAVA EDITION ONLY (Options 1-7, 8-9)
For PC, Mac, Linux players only. Bedrock players **cannot** join.

| Option | Type | Best For | RAM | Notes |
|--------|------|----------|-----|-------|
| [1] | Vanilla | Pure Minecraft | 2GB | No plugins/mods |
| [2] | Paper | Most users | 2-3GB | Optimized, plugin support |
| [3] | Spigot | Plugin servers | 2-3GB | Classic plugin platform |
| [4] | Purpur | Performance | 2-3GB | Extra optimization |
| [5] | Fabric | Mods | 3-4GB | Modern mod loader |
| [6] | Forge | Mods | 3-4GB | Traditional mods |
| [7] | NeoForge | Latest mods | 3-4GB | Newer Forge fork |
| [8] | BungeeCord | Network proxy | 1GB | Connects multiple servers |
| [9] | Velocity | Modern proxy | 1GB | Better than Bungee |

### BEDROCK EDITION ONLY (Option 10)
For mobile, console, Windows 10/11 Bedrock players. Java players **cannot** join.

| Option | Type | Best For | RAM | Port |
|--------|------|----------|-----|------|
| [10] | Bedrock | Mobile/Console | 1-2GB | 19132 |

- Native Pocket Edition server
- Works on: iOS, Android, Xbox, PlayStation, Nintendo Switch, Windows 10/11 Bedrock
- No plugins/mods like Java servers
- Lightweight and mobile-optimized

### CROSSPLAY - JAVA + BEDROCK TOGETHER! (Options 11-14)
**BOTH Java AND Bedrock players can join the SAME server!**

| Option | Type | Best For | RAM | Java Port | Bedrock Port |
|--------|------|----------|-----|-----------|--------------|
| [11] | Paper+Geyser | **Most Popular** | 3-4GB | 25565 | 19132 |
| [12] | Fabric+Geyser | Mods + Crossplay | 4-5GB | 25565 | 19132 |
| [13] | Purpur+Geyser | High Performance | 3-4GB | 25565 | 19132 |
| [14] | Spigot+Geyser | Classic Plugins | 3-4GB | 25565 | 19132 |

## 🎯 WHICH ONE SHOULD I CHOOSE?

### Just want Java players? → **[2] Paper**
- Most popular
- Best optimization
- Plugin support
- 2-3GB RAM

### Just want Bedrock (mobile) players? → **[10] Bedrock**
- Mobile devices, consoles
- Lightweight (1-2GB RAM)
- No Java needed on client

### Want BOTH Java + Bedrock? → **[11] Paper+Geyser**
- PC players AND mobile players together!
- Most stable crossplay option
- 3-4GB RAM recommended

### Want mods + crossplay? → **[12] Fabric+Geyser**
- Install Fabric mods
- Bedrock players can still join
- 4-5GB RAM recommended

### Want best performance + crossplay? → **[13] Purpur+Geyser**
- Highly optimized
- Both Java and Bedrock
- 3-4GB RAM

## 🔧 HOW CROSSPLAY WORKS

### Technology: Geyser + Floodgate

**Geyser** = Translation layer that converts Bedrock protocol ↔ Java protocol
**Floodgate** = Allows Bedrock players to join without Java account

### Ports:
- **Java players** connect to: `IP:25565` (TCP)
- **Bedrock players** connect to: `IP:19132` (UDP)

### What players see:
- Java players: Normal Java server
- Bedrock players: Appears as Bedrock server
- Both see each other in-game!

## 📋 DETAILED COMPARISON

### Paper+Geyser [11] ⭐ RECOMMENDED
**Pros:**
- ✅ Most stable crossplay
- ✅ Best plugin compatibility
- ✅ Actively maintained
- ✅ 3-4GB RAM enough
- ✅ Paper's optimizations

**Cons:**
- ❌ No mods (use plugins instead)

**Best for:**
- Crossplay survival servers
- Plugin-based servers
- Public servers
- First-time crossplay setup

### Fabric+Geyser [12]
**Pros:**
- ✅ Mod support (server-side mods)
- ✅ Modern mod ecosystem
- ✅ Performance mods available
- ✅ Crossplay enabled

**Cons:**
- ❌ Needs 4-5GB RAM
- ❌ Mods need to be server-side compatible
- ❌ Java players need matching mods

**Best for:**
- Modded servers with crossplay
- Technical players
- Custom gameplay with mods

**Note:** Bedrock players won't see mod content unless Geyser extensions are used!

### Purpur+Geyser [13]
**Pros:**
- ✅ Highest performance
- ✅ Extra configuration options
- ✅ Based on Paper (plugin compatible)
- ✅ Advanced optimization

**Cons:**
- ❌ May have slight compatibility issues with some plugins

**Best for:**
- Large player counts
- High-performance servers
- Experienced admins
- Competitive servers

### Spigot+Geyser [14]
**Pros:**
- ✅ Classic, well-known platform
- ✅ Wide plugin compatibility
- ✅ Stable and mature

**Cons:**
- ❌ Less optimized than Paper/Purpur
- ❌ Older codebase

**Best for:**
- Classic plugin servers
- Long-running servers
- Specific Spigot plugins

## 🚀 SETUP EXAMPLES

### Example 1: Friends Server (Mixed devices)
**Scenario:** You have 10 friends, some on PC, some on mobile

**Recommended:** [11] Paper+Geyser
```bash
bash msm.sh
[1] Create New Server
[11] Paper+Geyser
Name: friendsworld
Version: latest
RAM: 3072 (3GB)
```

**Why:** Easiest setup, works for everyone, stable.

### Example 2: Modded Survival (Some mobile friends)
**Scenario:** Modded Java server but want mobile friends to join

**Recommended:** [12] Fabric+Geyser
```bash
bash msm.sh
[1] Create New Server
[12] Fabric+Geyser
Name: moddedworld
Version: 1.20.4
RAM: 4096 (4GB)
```

**Then add mods to:** `~/.msm/servers/moddedworld/mods/`

**Why:** Fabric mods + crossplay. Mobile players see vanilla-ish experience.

### Example 3: Mobile-Only Server
**Scenario:** All players on phones/tablets

**Recommended:** [10] Bedrock
```bash
bash msm.sh
[1] Create New Server
[10] Bedrock
Name: mobileserver
RAM: 2048 (2GB)
```

**Why:** Native Bedrock = best performance for mobile. Lower RAM usage.

### Example 4: Large Public Server
**Scenario:** 50+ players, mixed devices, need best performance

**Recommended:** [13] Purpur+Geyser
```bash
bash msm.sh
[1] Create New Server
[13] Purpur+Geyser
Name: publicserver
Version: latest
RAM: 5120 (5GB)
```

**Why:** Maximum performance optimization for high player count.

## 📊 RAM REQUIREMENTS

| Players | Java Only | Crossplay | Bedrock Only |
|---------|-----------|-----------|--------------|
| 1-5 | 2GB | 3GB | 1GB |
| 5-10 | 2-3GB | 3-4GB | 2GB |
| 10-20 | 3-4GB | 4-5GB | 2-3GB |
| 20-50 | 4-6GB | 5-7GB | 3-4GB |
| 50+ | 6GB+ | 7GB+ | 4GB+ |

**Note:** Crossplay needs more RAM because Geyser translates between protocols.

## 🔌 CONNECTION INSTRUCTIONS

### For Java Edition Players:
```
Server Address: <your-ip>:25565
Example: 192.168.1.50:25565
```

### For Bedrock Edition Players:
```
Server Address: <your-ip>
Port: 19132
Example: 
  Address: 192.168.1.50
  Port: 19132
```

### Finding Your IP:
```bash
# On Android/Termux
ifconfig | grep "inet " | grep -v 127.0.0.1

# You'll see something like:
inet 192.168.1.50 netmask ...
```

## ⚙️ PLUGIN/MOD COMPATIBILITY

### Paper+Geyser [11]
- ✅ Spigot plugins
- ✅ Paper plugins
- ✅ Bukkit plugins
- ❌ Fabric/Forge mods

### Fabric+Geyser [12]
- ✅ Fabric mods (server-side)
- ✅ Some Fabric plugins
- ❌ Spigot/Bukkit plugins
- ❌ Forge mods

### Purpur+Geyser [13]
- ✅ Spigot plugins
- ✅ Paper plugins
- ✅ Purpur-specific plugins
- ❌ Mods

### Spigot+Geyser [14]
- ✅ Spigot plugins
- ✅ Bukkit plugins
- ❌ Paper-only plugins
- ❌ Mods

## 🎮 FEATURES COMPARISON

| Feature | Java Only | Bedrock Only | Crossplay |
|---------|-----------|--------------|-----------|
| Plugins | ✅ | ❌ | ✅ |
| Mods | ✅ (Forge/Fabric) | ❌ | ⚠️ (Limited) |
| Mobile Players | ❌ | ✅ | ✅ |
| PC/Mac Players | ✅ | ❌ | ✅ |
| Console Players | ❌ | ✅ | ✅ |
| RAM Usage | Medium | Low | High |
| Setup Difficulty | Easy | Easy | Medium |

## 🐛 KNOWN LIMITATIONS

### Bedrock Players on Crossplay Servers:
- May not see some plugin features (holograms, custom GUIs)
- Some commands might not work the same
- Emotes/character creator won't show to Java players
- Chat formatting may differ
- Some blocks/items may appear different

### Java Players on Crossplay Servers:
- No changes, plays like normal Java server

### Performance:
- Crossplay servers use ~20-30% more CPU
- Geyser adds ~200-500MB RAM overhead

## 🔧 AFTER SETUP

### Check if Geyser loaded:
```bash
# View server logs
tail -100 ~/.msm/servers/YOUR-SERVER/logs/latest.log | grep -i geyser

# Should see:
[Geyser-Spigot] Enabling Geyser-Spigot
[Geyser-Spigot] Started Geyser on 0.0.0.0:19132
```

### Configure Geyser:
```bash
# Spigot/Paper/Purpur servers:
nano ~/.msm/servers/YOUR-SERVER/plugins/Geyser-Spigot/config.yml

# Fabric servers:
nano ~/.msm/servers/YOUR-SERVER/config/Geyser-Fabric/config.yml
```

### Important Geyser settings:
```yaml
bedrock:
  address: 0.0.0.0
  port: 19132

remote:
  address: 127.0.0.1
  port: 25565
```

## ✅ TESTING CHECKLIST

- [ ] Server shows [RUNNING] status
- [ ] Port 25565 listening (Java)
- [ ] Port 19132 listening (Bedrock) - for crossplay/bedrock servers
- [ ] Log shows "Done" message
- [ ] Geyser loaded (check logs for crossplay)
- [ ] server-ip=0.0.0.0 in server.properties
- [ ] Can connect from localhost
- [ ] Can connect from other device on WiFi

### Run diagnostic:
```bash
bash diagnose.sh
# Should show all ✓ green checkmarks
```

## 🆘 TROUBLESHOOTING

### Bedrock players can't join crossplay server:
1. Check port 19132 is open:
   ```bash
   netstat -unp | grep 19132
   ```
2. Check Geyser loaded:
   ```bash
   tail ~/.msm/servers/YOUR-SERVER/logs/latest.log | grep Geyser
   ```
3. Verify Geyser config port is 19132

### Java players can join but Bedrock players time out:
- Bedrock uses **UDP** port 19132, not TCP!
- Some routers/firewalls block UDP
- Test on same WiFi first before internet access

### "Failed to connect to the server" (Bedrock):
- Make sure using port 19132 not 25565
- Bedrock requires separate port field in Add Server menu
- Double-check IP address is correct

## 📖 MORE HELP

- Full connection guide: `cat CONNECTION-FIX.md`
- Bedrock setup: `cat BEDROCK-CROSSPLAY.md`
- Run diagnostic: `bash diagnose.sh`
- Check status: `bash msm.sh` → [12] Server Status

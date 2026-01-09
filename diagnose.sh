#!/data/data/com.termux/files/usr/bin/bash
# Connection Diagnostic Tool

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

clear
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}    MINECRAFT SERVER CONNECTION DIAGNOSTIC${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

SERVERS_DIR="$HOME/.msm/servers"

# Check if any servers exist
if [ ! -d "$SERVERS_DIR" ] || [ -z "$(ls -A $SERVERS_DIR)" ]; then
    echo -e "${RED}✗ No servers found!${NC}"
    echo "  Create a server first: bash msm.sh → Option 1"
    exit 1
fi

# List servers
echo -e "${BOLD}${YELLOW}Available Servers:${NC}"
for server_dir in "$SERVERS_DIR"/*; do
    if [ -d "$server_dir" ]; then
        server_name=$(basename "$server_dir")
        
        # Check status
        if screen -list 2>/dev/null | grep -q "msm-$server_name"; then
            status="${GREEN}[RUNNING]${NC}"
        else
            status="${RED}[STOPPED]${NC}"
        fi
        
        # Get config
        if [ -f "$server_dir/msm_config.json" ]; then
            port=$(jq -r '.port // "25565"' "$server_dir/msm_config.json" 2>/dev/null)
            type=$(jq -r '.type // "Unknown"' "$server_dir/msm_config.json" 2>/dev/null)
            echo -e "  ${CYAN}→${NC} $server_name ${status} - Type: $type, Port: $port"
        else
            echo -e "  ${CYAN}→${NC} $server_name ${status}"
        fi
    fi
done

echo ""
echo -e "${YELLOW}Select server to diagnose:${NC}"
read -p "> " server_name

server_path="$SERVERS_DIR/$server_name"
if [ ! -d "$server_path" ]; then
    echo -e "${RED}✗ Server not found!${NC}"
    exit 1
fi

echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}    DIAGNOSTIC RESULTS FOR: $server_name${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

# Test 1: Screen session
echo -e "${BOLD}1. Screen Session:${NC}"
if screen -list 2>/dev/null | grep -q "msm-$server_name"; then
    echo -e "   ${GREEN}✓ Screen session exists${NC}"
    screen -list 2>/dev/null | grep "msm-$server_name" | sed 's/^/   /'
else
    echo -e "   ${RED}✗ No screen session found${NC}"
    echo -e "   ${YELLOW}→ Start server: bash msm.sh → Option 2${NC}"
fi

# Test 2: Java process
echo ""
echo -e "${BOLD}2. Java Server Process:${NC}"
if ps aux 2>/dev/null | grep -q "[j]ava.*server.jar"; then
    echo -e "   ${GREEN}✓ Java process running${NC}"
    ps aux 2>/dev/null | grep "[j]ava.*server.jar" | awk '{print "   PID: "$2" RAM: "$6"KB"}' | head -1
else
    echo -e "   ${RED}✗ No Java process found${NC}"
    echo -e "   ${YELLOW}→ Server may still be starting (wait 30-60s)${NC}"
fi

# Test 3: Port listening
echo ""
echo -e "${BOLD}3. Network Ports:${NC}"
if command -v netstat &> /dev/null; then
    ports=$(netstat -tulpn 2>/dev/null | grep -E ":(25565|19132)")
    if [ -n "$ports" ]; then
        echo -e "   ${GREEN}✓ Ports listening:${NC}"
        echo "$ports" | sed 's/^/   /'
    else
        echo -e "   ${RED}✗ No ports listening${NC}"
        echo -e "   ${YELLOW}→ Server not ready or failed to bind${NC}"
    fi
elif command -v ss &> /dev/null; then
    ports=$(ss -tulpn 2>/dev/null | grep -E ":(25565|19132)")
    if [ -n "$ports" ]; then
        echo -e "   ${GREEN}✓ Ports listening:${NC}"
        echo "$ports" | sed 's/^/   /'
    else
        echo -e "   ${RED}✗ No ports listening${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ netstat/ss not available${NC}"
fi

# Test 4: Server configuration
echo ""
echo -e "${BOLD}4. Server Configuration:${NC}"
if [ -f "$server_path/server.properties" ]; then
    server_ip=$(grep "^server-ip=" "$server_path/server.properties" 2>/dev/null | cut -d'=' -f2)
    server_port=$(grep "^server-port=" "$server_path/server.properties" 2>/dev/null | cut -d'=' -f2)
    online_mode=$(grep "^online-mode=" "$server_path/server.properties" 2>/dev/null | cut -d'=' -f2)
    
    if [ "$server_ip" = "0.0.0.0" ] || [ -z "$server_ip" ]; then
        echo -e "   ${GREEN}✓ server-ip: $server_ip (correct)${NC}"
    else
        echo -e "   ${RED}✗ server-ip: $server_ip (should be 0.0.0.0)${NC}"
        echo -e "   ${YELLOW}→ Fix: Edit $server_path/server.properties${NC}"
    fi
    
    echo -e "   ${CYAN}→ Port: $server_port${NC}"
    echo -e "   ${CYAN}→ Online mode: $online_mode${NC}"
else
    echo -e "   ${RED}✗ server.properties not found${NC}"
fi

# Test 5: Local IP addresses
echo ""
echo -e "${BOLD}5. Device IP Addresses:${NC}"
if command -v ifconfig &> /dev/null; then
    ips=$(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}')
    if [ -n "$ips" ]; then
        echo -e "   ${GREEN}✓ Available IPs:${NC}"
        echo "$ips" | while read ip; do
            echo -e "   ${CYAN}→ $ip${NC}"
        done
    else
        echo -e "   ${YELLOW}⚠ No network IPs found (only localhost)${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ ifconfig not available${NC}"
fi

# Test 6: Port connectivity
echo ""
echo -e "${BOLD}6. Port Connection Test:${NC}"
if [ -n "$server_port" ]; then
    if timeout 2 bash -c "</dev/tcp/localhost/$server_port" 2>/dev/null; then
        echo -e "   ${GREEN}✓ Port $server_port is accessible on localhost${NC}"
    else
        echo -e "   ${RED}✗ Cannot connect to port $server_port${NC}"
        echo -e "   ${YELLOW}→ Server may not be fully started${NC}"
    fi
fi

# Test 7: Recent logs
echo ""
echo -e "${BOLD}7. Recent Server Logs:${NC}"
if [ -f "$server_path/logs/latest.log" ]; then
    echo -e "   ${CYAN}Last 10 log lines:${NC}"
    tail -10 "$server_path/logs/latest.log" 2>/dev/null | sed 's/^/   /' | tail -10
    
    # Check for errors
    if grep -qi "error\|exception\|failed" "$server_path/logs/latest.log" 2>/dev/null; then
        echo ""
        echo -e "   ${RED}⚠ Errors detected in logs!${NC}"
        echo -e "   ${YELLOW}→ View full log: cat $server_path/logs/latest.log${NC}"
    fi
    
    # Check if done loading
    if grep -q "Done.*For help, type" "$server_path/logs/latest.log" 2>/dev/null; then
        echo -e "   ${GREEN}✓ Server finished loading${NC}"
    else
        echo -e "   ${YELLOW}⚠ Server may still be starting...${NC}"
    fi
else
    echo -e "   ${RED}✗ No log file found${NC}"
fi

# Summary and recommendations
echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}    CONNECTION INSTRUCTIONS${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

# Get server type
if [ -f "$server_path/msm_config.json" ]; then
    type=$(jq -r '.type // "Unknown"' "$server_path/msm_config.json" 2>/dev/null)
    
    if [[ "$type" == *"Geyser"* ]] || [[ "$type" == *"Crossplay"* ]]; then
        echo -e "${BOLD}${MAGENTA}🌐 CROSSPLAY SERVER (Java + Bedrock)${NC}"
        echo ""
        echo -e "${GREEN}Java Edition players:${NC}"
        if [ -n "$ips" ]; then
            echo "$ips" | while read ip; do
                echo -e "   ${CYAN}→ $ip:${server_port:-25565}${NC}"
            done
        fi
        echo ""
        echo -e "${GREEN}Bedrock Edition players:${NC}"
        if [ -n "$ips" ]; then
            echo "$ips" | while read ip; do
                echo -e "   ${CYAN}→ $ip:19132${NC}"
            done
        fi
    elif [[ "$type" == "Bedrock" ]]; then
        echo -e "${BOLD}${MAGENTA}📱 BEDROCK SERVER (Pocket Edition)${NC}"
        echo ""
        if [ -n "$ips" ]; then
            echo "$ips" | while read ip; do
                echo -e "   ${CYAN}→ $ip:19132${NC}"
            done
        fi
    else
        echo -e "${BOLD}${GREEN}☕ JAVA EDITION SERVER${NC}"
        echo ""
        if [ -n "$ips" ]; then
            echo "$ips" | while read ip; do
                echo -e "   ${CYAN}→ $ip:${server_port:-25565}${NC}"
            done
        fi
    fi
fi

echo ""
echo -e "${YELLOW}📖 Full troubleshooting guide:${NC}"
echo -e "   cat CONNECTION-FIX.md"
echo ""
echo -e "${YELLOW}💡 Quick fixes:${NC}"
echo -e "   • Wait 30-60s for server to fully start"
echo -e "   • Both devices must be on SAME WiFi network"
echo -e "   • Use local IP (192.168.x.x) not external IP"
echo -e "   • Check server.properties has server-ip=0.0.0.0"
echo ""

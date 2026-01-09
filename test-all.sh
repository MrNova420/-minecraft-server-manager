#!/data/data/com.termux/files/usr/bin/bash
# Complete System Validation & Auto-Fix

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${CYAN}════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  MINECRAFT SERVER MANAGER - SYSTEM CHECK${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ERRORS=0
WARNINGS=0

# Test function
test_item() {
    local name="$1"
    local command="$2"
    
    echo -ne "${CYAN}Testing:${NC} $name ... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Warning function
warn_item() {
    local name="$1"
    local command="$2"
    
    echo -ne "${CYAN}Checking:${NC} $name ... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠${NC}"
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

echo -e "${BOLD}1. Core Files${NC}"
test_item "Main script (msm.sh)" "[ -f '$SCRIPT_DIR/msm.sh' ]"
test_item "Install script" "[ -f '$SCRIPT_DIR/install.sh' ]"
test_item "Server creator" "[ -f '$SCRIPT_DIR/core/server_creator.py' ]"
test_item "Server manager" "[ -f '$SCRIPT_DIR/core/server_manager.py' ]"
test_item "Plugin manager" "[ -f '$SCRIPT_DIR/core/plugin_manager.py' ]"
test_item "Backup manager" "[ -f '$SCRIPT_DIR/core/backup_manager.py' ]"
test_item "Resource monitor" "[ -f '$SCRIPT_DIR/core/resource_monitor.py' ]"
test_item "Performance tuner" "[ -f '$SCRIPT_DIR/core/performance_tuner.py' ]"
test_item "Web panel" "[ -f '$SCRIPT_DIR/core/web_panel.py' ]"
test_item "Server status" "[ -f '$SCRIPT_DIR/core/server_status.py' ]"
test_item "Settings manager" "[ -f '$SCRIPT_DIR/core/settings.py' ]"

echo ""
echo -e "${BOLD}2. Utility Scripts${NC}"
test_item "Diagnostic tool" "[ -f '$SCRIPT_DIR/diagnose.sh' ]"
test_item "Connection info" "[ -f '$SCRIPT_DIR/server-info.sh' ]"
test_item "Fix script" "[ -f '$SCRIPT_DIR/fix.sh' ]"
warn_item "Demo script" "[ -f '$SCRIPT_DIR/demo.sh' ]"

echo ""
echo -e "${BOLD}3. Documentation${NC}"
test_item "README" "[ -f '$SCRIPT_DIR/README.md' ]"
test_item "Connection fix guide" "[ -f '$SCRIPT_DIR/CONNECTION-FIX.md' ]"
test_item "Server types guide" "[ -f '$SCRIPT_DIR/SERVER-TYPES-GUIDE.md' ]"
test_item "Bedrock/Crossplay guide" "[ -f '$SCRIPT_DIR/BEDROCK-CROSSPLAY.md' ]"

echo ""
echo -e "${BOLD}4. System Dependencies${NC}"
test_item "Python3" "command -v python3"
test_item "Java" "command -v java"
test_item "Screen" "command -v screen"
test_item "Git" "command -v git"
test_item "jq" "command -v jq"
warn_item "wget" "command -v wget"
warn_item "curl" "command -v curl"

echo ""
echo -e "${BOLD}5. Python Modules${NC}"
test_item "psutil" "python3 -c 'import psutil'"
test_item "requests" "python3 -c 'import requests'"
test_item "flask" "python3 -c 'import flask'"
test_item "tqdm" "python3 -c 'import tqdm'"
test_item "colorama" "python3 -c 'import colorama'"

echo ""
echo -e "${BOLD}6. Directory Structure${NC}"
test_item "Data directory" "[ -d '$HOME/.msm' ]"
test_item "Servers directory" "[ -d '$HOME/.msm/servers' ]"
test_item "Backups directory" "[ -d '$HOME/.msm/backups' ]"
test_item "Plugins directory" "[ -d '$HOME/.msm/plugins' ]"
test_item "Mods directory" "[ -d '$HOME/.msm/mods' ]"

echo ""
echo -e "${BOLD}7. Script Permissions${NC}"
test_item "msm.sh executable" "[ -x '$SCRIPT_DIR/msm.sh' ]"
test_item "diagnose.sh executable" "[ -x '$SCRIPT_DIR/diagnose.sh' ]"
test_item "install.sh executable" "[ -x '$SCRIPT_DIR/install.sh' ]"

echo ""
echo -e "${BOLD}8. Python Scripts Syntax${NC}"
echo -ne "${CYAN}Testing:${NC} server_creator.py syntax ... "
if python3 -m py_compile "$SCRIPT_DIR/core/server_creator.py" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo -ne "${CYAN}Testing:${NC} plugin_manager.py syntax ... "
if python3 -m py_compile "$SCRIPT_DIR/core/plugin_manager.py" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo -ne "${CYAN}Testing:${NC} web_panel.py syntax ... "
if python3 -m py_compile "$SCRIPT_DIR/core/web_panel.py" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo -e "${BOLD}9. Network Capabilities${NC}"
warn_item "Internet connection" "ping -c 1 8.8.8.8 2>/dev/null"
warn_item "DNS resolution" "nslookup google.com 2>/dev/null"
test_item "Network interface" "ifconfig 2>/dev/null | grep -q 'inet '"

echo ""
echo -e "${BOLD}10. Java Environment${NC}"
if command -v java &>/dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo -e "${CYAN}Java version:${NC} $JAVA_VERSION"
    
    # Check if Java 17+
    if java -version 2>&1 | grep -q "version \"1[7-9]\|version \"[2-9][0-9]"; then
        echo -e "${GREEN}✓${NC} Java 17+ detected"
    else
        echo -e "${YELLOW}⚠${NC} Java version may be too old (need 17+)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}✗${NC} Java not installed!"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo -e "${BOLD}11. Available RAM${NC}"
if command -v free &>/dev/null; then
    TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
    FREE_RAM=$(free -m | awk '/^Mem:/{print $7}')
    echo -e "${CYAN}Total RAM:${NC} ${TOTAL_RAM}MB"
    echo -e "${CYAN}Available RAM:${NC} ${FREE_RAM}MB"
    
    if [ "$FREE_RAM" -lt 1024 ]; then
        echo -e "${RED}✗${NC} Less than 1GB free RAM!"
        ERRORS=$((ERRORS + 1))
    elif [ "$FREE_RAM" -lt 2048 ]; then
        echo -e "${YELLOW}⚠${NC} Less than 2GB free RAM (recommended: 2GB+)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} Sufficient RAM available"
    fi
fi

echo ""
echo -e "${BOLD}12. Storage Space${NC}"
if command -v df &>/dev/null; then
    FREE_SPACE=$(df -h ~ | awk 'NR==2 {print $4}')
    echo -e "${CYAN}Free space:${NC} $FREE_SPACE"
    
    FREE_SPACE_MB=$(df -m ~ | awk 'NR==2 {print $4}')
    if [ "$FREE_SPACE_MB" -lt 1024 ]; then
        echo -e "${RED}✗${NC} Less than 1GB free space!"
        ERRORS=$((ERRORS + 1))
    elif [ "$FREE_SPACE_MB" -lt 5120 ]; then
        echo -e "${YELLOW}⚠${NC} Less than 5GB free space"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} Sufficient storage space"
    fi
fi

echo ""
echo -e "${BOLD}${CYAN}════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  TEST RESULTS${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}System is ready to run Minecraft servers!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}${BOLD}⚠ PASSED WITH WARNINGS${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo -e "System should work but some features may be limited"
    exit 0
else
    echo -e "${RED}${BOLD}✗ FAILED${NC}"
    echo -e "${RED}Errors: $ERRORS${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo ""
    echo -e "${YELLOW}To fix issues, run:${NC}"
    echo -e "  bash install.sh"
    exit 1
fi

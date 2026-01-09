#!/usr/bin/env bash
# Fix and test script for Minecraft Server Manager

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    MSM - Diagnostic & Fix Tool                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

DATA_DIR="$HOME/.msm"
SERVERS_DIR="$DATA_DIR/servers"

echo -e "${CYAN}[1/6]${NC} Checking directory structure..."
if [ ! -d "$DATA_DIR" ]; then
    echo -e "${YELLOW}  Creating data directory...${NC}"
    mkdir -p "$DATA_DIR" "$SERVERS_DIR" "$DATA_DIR/backups" "$DATA_DIR/plugins" "$DATA_DIR/mods"
fi
echo -e "${GREEN}  ✓ Directories OK${NC}"

echo ""
echo -e "${CYAN}[2/6]${NC} Checking dependencies..."

# Check Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}  ✓ Python3 installed${NC}"
else
    echo -e "${RED}  ✗ Python3 not found${NC}"
    echo -e "${YELLOW}  Installing Python...${NC}"
    pkg install -y python
fi

# Check required Python packages
echo -e "${CYAN}  Checking Python packages...${NC}"
python3 -c "import psutil" 2>/dev/null || pip install psutil
python3 -c "import requests" 2>/dev/null || pip install requests
python3 -c "import flask" 2>/dev/null || pip install flask flask-cors
python3 -c "import tqdm" 2>/dev/null || pip install tqdm
echo -e "${GREEN}  ✓ Python packages OK${NC}"

# Check screen
if command -v screen &> /dev/null; then
    echo -e "${GREEN}  ✓ Screen installed${NC}"
else
    echo -e "${YELLOW}  Installing screen...${NC}"
    pkg install -y screen
fi

echo ""
echo -e "${CYAN}[3/6]${NC} Checking file permissions..."
chmod +x *.sh 2>/dev/null
chmod +x core/*.py 2>/dev/null
echo -e "${GREEN}  ✓ Permissions set${NC}"

echo ""
echo -e "${CYAN}[4/6]${NC} Testing Python modules..."
ERROR=0

for script in core/*.py; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        echo -e "${GREEN}  ✓ $(basename $script)${NC}"
    else
        echo -e "${RED}  ✗ $(basename $script) - Syntax error${NC}"
        ERROR=1
    fi
done

if [ $ERROR -eq 1 ]; then
    echo -e "${RED}Fix Python syntax errors before continuing${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}[5/6]${NC} Testing server operations..."

# Test if we can create a test config
TEST_SERVER="$SERVERS_DIR/test-server"
if [ -d "$TEST_SERVER" ]; then
    echo -e "${YELLOW}  Test server already exists, skipping...${NC}"
else
    echo -e "${CYAN}  Creating test server structure...${NC}"
    mkdir -p "$TEST_SERVER"
    cat > "$TEST_SERVER/msm_config.json" << 'EOF'
{
  "name": "test-server",
  "type": "Paper",
  "version": "1.20.4",
  "ram": 2048,
  "cores": 2,
  "jar_file": "server.jar",
  "port": 25565
}
EOF
    echo -e "${GREEN}  ✓ Test server created${NC}"
fi

echo ""
echo -e "${CYAN}[6/6]${NC} Testing web panel..."
if python3 -c "from flask import Flask; from flask_cors import CORS" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Flask modules OK${NC}"
else
    echo -e "${YELLOW}  Installing Flask...${NC}"
    pip install flask flask-cors
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                 DIAGNOSTIC COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}All systems ready!${NC}"
echo ""
echo "Quick Test Commands:"
echo -e "  ${CYAN}•${NC} Main Menu:      ./msm.sh"
echo -e "  ${CYAN}•${NC} Server Status:  python3 core/server_status.py"
echo -e "  ${CYAN}•${NC} List Servers:   python3 core/server_manager.py list"
echo -e "  ${CYAN}•${NC} Web Panel:      python3 core/web_panel.py"
echo ""

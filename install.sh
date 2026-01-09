#!/data/data/com.termux/files/usr/bin/bash
# Minecraft Server Manager - Advanced Installation Script
# For Android Termux - Professional Server Hosting Solution

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Minecraft Server Manager - Professional Edition       ║"
echo "║    Advanced Android Server Hosting Platform              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="$HOME/minecraft-server-manager"
DATA_DIR="$HOME/.msm"
SERVERS_DIR="$DATA_DIR/servers"
BACKUPS_DIR="$DATA_DIR/backups"
PLUGINS_DIR="$DATA_DIR/plugins"
MODS_DIR="$DATA_DIR/mods"

echo -e "${CYAN}[INFO]${NC} Creating directory structure..."
mkdir -p "$DATA_DIR" "$SERVERS_DIR" "$BACKUPS_DIR" "$PLUGINS_DIR" "$MODS_DIR"

echo -e "${CYAN}[INFO]${NC} Updating Termux packages..."
yes | pkg update 2>/dev/null
yes | pkg upgrade 2>/dev/null

echo -e "${CYAN}[INFO]${NC} Installing core dependencies..."
yes | pkg install -y openjdk-17 python wget curl git tar gzip unzip screen htop ncurses-utils termux-api jq 2>/dev/null

echo -e "${CYAN}[INFO]${NC} Installing Python dependencies..."
pip install --upgrade pip 2>/dev/null
pip install psutil requests tqdm colorama flask flask-cors pyyaml 2>/dev/null

echo -e "${CYAN}[INFO]${NC} Setting up permissions..."
termux-setup-storage

echo -e "${CYAN}[INFO]${NC} Creating configuration file..."
cat > "$DATA_DIR/config.json" << 'EOF'
{
  "default_java_version": "17",
  "default_ram": "2048",
  "default_cores": "2",
  "auto_backup": true,
  "backup_interval": 3600,
  "max_backups": 5,
  "monitoring": true,
  "web_interface": true,
  "web_port": 8080
}
EOF

echo -e "${CYAN}[INFO]${NC} Setting up executable permissions..."
chmod +x "$INSTALL_DIR"/*.sh 2>/dev/null
chmod +x "$INSTALL_DIR"/core/*.py 2>/dev/null

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Installation Complete!                         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Quick Start:${NC}"
echo -e "  ${CYAN}1.${NC} Run: ${GREEN}./msm.sh${NC}"
echo -e "  ${CYAN}2.${NC} Create a new server using the interactive menu"
echo -e "  ${CYAN}3.${NC} Configure RAM, CPU cores, and server type"
echo -e "  ${CYAN}4.${NC} Start your server and enjoy!"
echo ""

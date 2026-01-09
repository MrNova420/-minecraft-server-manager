#!/data/data/com.termux/files/usr/bin/bash
# Minecraft Server Manager - Main Control Script
# Professional Android Server Hosting Platform

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Directories
DATA_DIR="$HOME/.msm"
SERVERS_DIR="$DATA_DIR/servers"
BACKUPS_DIR="$DATA_DIR/backups"
CONFIG_FILE="$DATA_DIR/config.json"

# Functions
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║       MINECRAFT SERVER MANAGER - PROFESSIONAL EDITION        ║"
    echo "║                                                              ║"
    echo "║          Advanced Android Server Hosting Platform           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_menu() {
    echo -e "${BOLD}${CYAN}═══════════════════ MAIN MENU ═══════════════════${NC}"
    echo ""
    echo -e "  ${GREEN}[1]${NC} Create New Server"
    echo -e "  ${GREEN}[2]${NC} Manage Existing Servers"
    echo -e "  ${GREEN}[3]${NC} Start Server"
    echo -e "  ${GREEN}[4]${NC} Stop Server"
    echo -e "  ${GREEN}[5]${NC} Server Console"
    echo -e "  ${GREEN}[6]${NC} Resource Monitor"
    echo -e "  ${GREEN}[7]${NC} Plugin/Mod Manager"
    echo -e "  ${GREEN}[8]${NC} Backup Manager"
    echo -e "  ${GREEN}[9]${NC} Performance Tuning"
    echo -e "  ${GREEN}[10]${NC} Web Control Panel"
    echo -e "  ${GREEN}[11]${NC} System Settings"
    echo -e "  ${GREEN}[12]${NC} Server Status"
    echo -e "  ${GREEN}[13]${NC} Connection Info (How to Connect)"
    echo -e "  ${RED}[0]${NC} Exit"
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo ""
}

list_servers() {
    echo -e "${CYAN}[INFO]${NC} Available servers:"
    if [ -d "$SERVERS_DIR" ] && [ "$(ls -A $SERVERS_DIR 2>/dev/null)" ]; then
        local i=1
        for server in "$SERVERS_DIR"/*; do
            if [ -d "$server" ]; then
                local server_name=$(basename "$server")
                local status=$(check_server_status "$server_name")
                
                # Get server info
                if [ -f "$server/msm_config.json" ]; then
                    local port=$(jq -r '.port' "$server/msm_config.json" 2>/dev/null || echo "25565")
                    local ram=$(jq -r '.ram' "$server/msm_config.json" 2>/dev/null || echo "unknown")
                    local type=$(jq -r '.type' "$server/msm_config.json" 2>/dev/null || echo "unknown")
                    echo -e "  ${GREEN}[$i]${NC} $server_name ${status}"
                    echo -e "      Type: $type | RAM: ${ram}MB | Port: $port"
                else
                    echo -e "  ${GREEN}[$i]${NC} $server_name ${status}"
                fi
                ((i++))
            fi
        done
    else
        echo -e "  ${YELLOW}No servers found${NC}"
    fi
}

check_server_status() {
    local server_name=$1
    if screen -list | grep -q "msm-$server_name"; then
        echo -e "${GREEN}[RUNNING]${NC}"
    else
        echo -e "${RED}[STOPPED]${NC}"
    fi
}

create_server() {
    show_banner
    echo -e "${BOLD}${CYAN}═══════════ CREATE NEW SERVER ═══════════${NC}"
    echo ""
    
    # Server name
    echo -e "${YELLOW}Enter server name:${NC}"
    read -p "> " server_name
    
    if [ -z "$server_name" ]; then
        echo -e "${RED}[ERROR]${NC} Server name cannot be empty"
        sleep 2
        return
    fi
    
    if [ -d "$SERVERS_DIR/$server_name" ]; then
        echo -e "${RED}[ERROR]${NC} Server already exists"
        sleep 2
        return
    fi
    
    # Server type
    echo ""
    echo -e "${YELLOW}Select server type:${NC}"
    echo -e "  ${GREEN}[1]${NC} Vanilla"
    echo -e "  ${GREEN}[2]${NC} Paper (Optimized - Recommended)"
    echo -e "  ${GREEN}[3]${NC} Spigot"
    echo -e "  ${GREEN}[4]${NC} Purpur (Best Performance)"
    echo -e "  ${GREEN}[5]${NC} Fabric (Mods)"
    echo -e "  ${GREEN}[6]${NC} Forge (Mods)"
    echo -e "  ${GREEN}[7]${NC} NeoForge (Latest Mods)"
    echo -e "  ${GREEN}[8]${NC} BungeeCord (Proxy)"
    echo -e "  ${GREEN}[9]${NC} Velocity (Modern Proxy)"
    read -p "> " server_type
    
    # Minecraft version
    echo ""
    echo -e "${YELLOW}Enter Minecraft version (e.g., 1.20.4, 1.19.4, latest):${NC}"
    read -p "> " mc_version
    [ -z "$mc_version" ] && mc_version="latest"
    
    # RAM allocation
    echo ""
    echo -e "${YELLOW}Enter RAM allocation in MB (recommended: 2048-4096):${NC}"
    read -p "> " ram
    [ -z "$ram" ] && ram="2048"
    
    # CPU cores
    echo ""
    echo -e "${YELLOW}Enter CPU cores to use (1-$(nproc)):${NC}"
    read -p "> " cores
    [ -z "$cores" ] && cores="2"
    
    # Create server
    python3 "$(dirname "$0")/core/server_creator.py" \
        --name "$server_name" \
        --type "$server_type" \
        --version "$mc_version" \
        --ram "$ram" \
        --cores "$cores"
    
    echo ""
    read -p "Press Enter to continue..." dummy
}

start_server() {
    show_banner
    echo -e "${BOLD}${CYAN}═══════════ START SERVER ═══════════${NC}"
    echo ""
    list_servers
    echo ""
    echo -e "${YELLOW}Enter server name to start:${NC}"
    read -p "> " server_name
    
    if [ -z "$server_name" ]; then
        return
    fi
    
    if [ ! -d "$SERVERS_DIR/$server_name" ]; then
        echo -e "${RED}[ERROR]${NC} Server not found"
        read -p "Press Enter to continue..." dummy
        return
    fi
    
    if screen -list | grep -q "msm-$server_name"; then
        echo -e "${YELLOW}[WARN]${NC} Server is already running"
        read -p "Press Enter to continue..." dummy
        return
    fi
    
    echo ""
    echo -e "${CYAN}[INFO]${NC} Starting server..."
    python3 "$(dirname "$0")/core/server_manager.py" start "$server_name"
    
    echo ""
    read -p "Press Enter to continue..." dummy
}

stop_server() {
    show_banner
    echo -e "${BOLD}${CYAN}═══════════ STOP SERVER ═══════════${NC}"
    echo ""
    list_servers
    echo ""
    echo -e "${YELLOW}Enter server name to stop:${NC}"
    read -p "> " server_name
    
    if [ -z "$server_name" ]; then
        return
    fi
    
    if ! screen -list | grep -q "msm-$server_name"; then
        echo -e "${YELLOW}[WARN]${NC} Server is not running"
        read -p "Press Enter to continue..." dummy
        return
    fi
    
    echo ""
    echo -e "${CYAN}[INFO]${NC} Stopping server..."
    python3 "$(dirname "$0")/core/server_manager.py" stop "$server_name"
    
    echo ""
    read -p "Press Enter to continue..." dummy
}

server_console() {
    show_banner
    echo -e "${BOLD}${CYAN}═══════════ SERVER CONSOLE ═══════════${NC}"
    echo ""
    list_servers
    echo ""
    echo -e "${YELLOW}Enter server name:${NC}"
    read -p "> " server_name
    
    if [ -z "$server_name" ]; then
        return
    fi
    
    if ! screen -list | grep -q "msm-$server_name"; then
        echo -e "${RED}[ERROR]${NC} Server is not running"
        read -p "Press Enter to continue..." dummy
        return
    fi
    
    echo -e "${CYAN}[INFO]${NC} Connecting to server console..."
    echo -e "${YELLOW}Press Ctrl+A then D to detach${NC}"
    sleep 2
    screen -r "msm-$server_name"
}

resource_monitor() {
    python3 "$(dirname "$0")/core/resource_monitor.py"
}

plugin_manager() {
    python3 "$(dirname "$0")/core/plugin_manager.py"
}

backup_manager() {
    python3 "$(dirname "$0")/core/backup_manager.py"
}

performance_tuning() {
    python3 "$(dirname "$0")/core/performance_tuner.py"
}

web_panel() {
    show_banner
    echo -e "${BOLD}${CYAN}═══════════ WEB CONTROL PANEL ═══════════${NC}"
    echo ""
    echo -e "${CYAN}[INFO]${NC} Starting web control panel..."
    python3 "$(dirname "$0")/core/web_panel.py"
}

server_status() {
    python3 "$(dirname "$0")/core/server_status.py"
}

system_settings() {
    python3 "$(dirname "$0")/core/settings.py"
}

# Main loop
while true; do
    show_banner
    show_menu
    read -p "Select option: " choice
    
    case $choice in
        1) create_server ;;
        2) python3 "$(dirname "$0")/core/server_manager.py" manage ;;
        3) start_server ;;
        4) stop_server ;;
        5) server_console ;;
        6) resource_monitor ;;
        7) plugin_manager ;;
        8) backup_manager ;;
        9) performance_tuning ;;
        10) web_panel ;;
        11) system_settings ;;
        12) server_status ;;
        13) bash "$(dirname "$0")/server-info.sh" ;;
        0) 
            clear
            echo -e "${GREEN}Thank you for using Minecraft Server Manager!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}[ERROR]${NC} Invalid option"
            sleep 1
            ;;
    esac
done

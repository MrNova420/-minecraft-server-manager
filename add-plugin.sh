#!/data/data/com.termux/files/usr/bin/bash
# Easy Plugin/Mod Installer

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

SERVERS_DIR="$HOME/.msm/servers"

clear
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}    PLUGIN & MOD INSTALLER${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
echo ""

# List servers
if [ ! -d "$SERVERS_DIR" ] || [ -z "$(ls -A $SERVERS_DIR 2>/dev/null)" ]; then
    echo -e "${RED}✗ No servers found!${NC}"
    echo "Create a server first: bash msm.sh → [1] Create New Server"
    exit 1
fi

echo -e "${BOLD}${YELLOW}Your Servers:${NC}"
i=1
declare -a server_list
for server_dir in "$SERVERS_DIR"/*; do
    if [ -d "$server_dir" ]; then
        server_name=$(basename "$server_dir")
        server_list[$i]="$server_name"
        
        # Get server type
        if [ -f "$server_dir/msm_config.json" ]; then
            type=$(jq -r '.type // "Unknown"' "$server_dir/msm_config.json" 2>/dev/null)
            echo -e "  ${GREEN}[$i]${NC} $server_name ${CYAN}($type)${NC}"
        else
            echo -e "  ${GREEN}[$i]${NC} $server_name"
        fi
        i=$((i + 1))
    fi
done

echo ""
echo -e "${YELLOW}Select server:${NC}"
read -p "> " server_choice

if [ -z "${server_list[$server_choice]}" ]; then
    echo -e "${RED}✗ Invalid selection!${NC}"
    exit 1
fi

SERVER_NAME="${server_list[$server_choice]}"
SERVER_PATH="$SERVERS_DIR/$SERVER_NAME"

# Detect server type
if [ -f "$SERVER_PATH/msm_config.json" ]; then
    SERVER_TYPE=$(jq -r '.type' "$SERVER_PATH/msm_config.json" 2>/dev/null)
else
    echo -e "${RED}✗ Cannot detect server type!${NC}"
    exit 1
fi

echo ""
echo -e "${BOLD}${CYAN}Server: ${SERVER_NAME}${NC}"
echo -e "${BOLD}${CYAN}Type: ${SERVER_TYPE}${NC}"
echo ""

# Determine if plugins or mods
if [[ "$SERVER_TYPE" == *"Fabric"* ]] || [[ "$SERVER_TYPE" == *"Forge"* ]] || [[ "$SERVER_TYPE" == *"NeoForge"* ]]; then
    MODE="mods"
    TARGET_DIR="$SERVER_PATH/mods"
    echo -e "${MAGENTA}This is a MOD server${NC}"
elif [[ "$SERVER_TYPE" == "Bedrock" ]]; then
    echo -e "${RED}✗ Bedrock servers don't support plugins/mods installation this way${NC}"
    exit 1
else
    MODE="plugins"
    TARGET_DIR="$SERVER_PATH/plugins"
    echo -e "${MAGENTA}This is a PLUGIN server${NC}"
fi

mkdir -p "$TARGET_DIR"

echo ""
echo -e "${BOLD}${YELLOW}Installation Options:${NC}"
echo -e "  ${GREEN}[1]${NC} Install from URL"
echo -e "  ${GREEN}[2]${NC} Install from file"
echo -e "  ${GREEN}[3]${NC} Install popular ${MODE}"
echo -e "  ${GREEN}[4]${NC} List installed ${MODE}"
echo -e "  ${GREEN}[5]${NC} Remove a ${MODE%s}"
echo -e "  ${RED}[0]${NC} Back"
echo ""
read -p "> " choice

case $choice in
    1)
        # Install from URL
        echo ""
        echo -e "${YELLOW}Enter direct download URL:${NC}"
        echo -e "${CYAN}(Must be .jar file link)${NC}"
        read -p "> " url
        
        if [ -z "$url" ]; then
            echo -e "${RED}✗ No URL provided!${NC}"
            exit 1
        fi
        
        filename=$(basename "$url")
        if [[ ! "$filename" == *.jar ]]; then
            filename="download.jar"
        fi
        
        echo ""
        echo -e "${CYAN}Downloading...${NC}"
        if curl -L -o "$TARGET_DIR/$filename" "$url"; then
            echo -e "${GREEN}✓ Installed: $filename${NC}"
            echo -e "${YELLOW}→ Restart server to load${NC}"
        else
            echo -e "${RED}✗ Download failed!${NC}"
        fi
        ;;
        
    2)
        # Install from file
        echo ""
        echo -e "${YELLOW}Enter full path to .jar file:${NC}"
        read -p "> " filepath
        
        if [ ! -f "$filepath" ]; then
            echo -e "${RED}✗ File not found!${NC}"
            exit 1
        fi
        
        if [[ ! "$filepath" == *.jar ]]; then
            echo -e "${RED}✗ Not a .jar file!${NC}"
            exit 1
        fi
        
        cp "$filepath" "$TARGET_DIR/"
        echo -e "${GREEN}✓ Installed: $(basename $filepath)${NC}"
        echo -e "${YELLOW}→ Restart server to load${NC}"
        ;;
        
    3)
        # Popular plugins/mods
        echo ""
        echo -e "${BOLD}${MAGENTA}Popular ${MODE^}:${NC}"
        echo ""
        
        if [ "$MODE" = "plugins" ]; then
            echo -e "${BOLD}${CYAN}━━━ Essential Plugins ━━━${NC}"
            echo -e "  ${GREEN}[1]${NC} EssentialsX - Commands, warps, kits"
            echo -e "  ${GREEN}[2]${NC} LuckPerms - Permission management"
            echo -e "  ${GREEN}[3]${NC} WorldEdit - World editing"
            echo -e "  ${GREEN}[4]${NC} WorldGuard - Area protection"
            echo -e "  ${GREEN}[5]${NC} Vault - Economy API"
            echo ""
            echo -e "${BOLD}${CYAN}━━━ Gameplay Plugins ━━━${NC}"
            echo -e "  ${GREEN}[6]${NC} CoreProtect - Anti-grief logging"
            echo -e "  ${GREEN}[7]${NC} Dynmap - Live web map"
            echo -e "  ${GREEN}[8]${NC} Citizens - NPC plugin"
            echo -e "  ${GREEN}[9]${NC} ChestShop - Player shops"
            echo -e "  ${GREEN}[10]${NC} Multiverse-Core - Multiple worlds"
            echo ""
            
            read -p "Select plugin (or 0 to cancel): " plugin_choice
            
            case $plugin_choice in
                1) 
                    curl -L -o "$TARGET_DIR/EssentialsX.jar" \
                        "https://github.com/EssentialsX/Essentials/releases/download/2.20.1/EssentialsX-2.20.1.jar"
                    ;;
                2)
                    curl -L -o "$TARGET_DIR/LuckPerms.jar" \
                        "https://download.luckperms.net/1542/bukkit/loader/LuckPerms-Bukkit-5.4.139.jar"
                    ;;
                3)
                    curl -L -o "$TARGET_DIR/WorldEdit.jar" \
                        "https://dev.bukkit.org/projects/worldedit/files/latest"
                    ;;
                4)
                    curl -L -o "$TARGET_DIR/WorldGuard.jar" \
                        "https://dev.bukkit.org/projects/worldguard/files/latest"
                    ;;
                5)
                    curl -L -o "$TARGET_DIR/Vault.jar" \
                        "https://github.com/MilkBowl/Vault/releases/download/1.7.3/Vault.jar"
                    ;;
                6)
                    curl -L -o "$TARGET_DIR/CoreProtect.jar" \
                        "https://github.com/PlayPro/CoreProtect/releases/download/22.4/CoreProtect-22.4.jar"
                    ;;
                7)
                    echo -e "${YELLOW}Dynmap is large (~20MB), continue? (y/n)${NC}"
                    read -p "> " confirm
                    if [ "$confirm" = "y" ]; then
                        curl -L -o "$TARGET_DIR/Dynmap.jar" \
                            "https://github.com/webbukkit/dynmap/releases/download/v3.7/Dynmap-3.7-spigot.jar"
                    fi
                    ;;
                8)
                    curl -L -o "$TARGET_DIR/Citizens.jar" \
                        "https://ci.citizensnpcs.co/job/Citizens2/lastSuccessfulBuild/artifact/dist/target/Citizens-2.0.35-b3504.jar"
                    ;;
                9)
                    curl -L -o "$TARGET_DIR/ChestShop.jar" \
                        "https://github.com/ChestShop-authors/ChestShop-3/releases/download/3.12.3/ChestShop.jar"
                    ;;
                10)
                    curl -L -o "$TARGET_DIR/Multiverse-Core.jar" \
                        "https://dev.bukkit.org/projects/multiverse-core/files/latest"
                    ;;
                0)
                    exit 0
                    ;;
                *)
                    echo -e "${RED}✗ Invalid selection!${NC}"
                    exit 1
                    ;;
            esac
            
            echo -e "${GREEN}✓ Plugin installed!${NC}"
            echo -e "${YELLOW}→ Restart server to load${NC}"
            
        else
            # Fabric mods
            echo -e "${BOLD}${CYAN}━━━ Performance Mods ━━━${NC}"
            echo -e "  ${GREEN}[1]${NC} Fabric API (Required for most mods)"
            echo -e "  ${GREEN}[2]${NC} Lithium - Server optimization"
            echo -e "  ${GREEN}[3]${NC} Phosphor - Lighting optimization"
            echo -e "  ${GREEN}[4]${NC} Carpet - Technical utilities"
            echo ""
            echo -e "${CYAN}Note: Download mods from CurseForge/Modrinth manually${NC}"
            echo -e "${CYAN}Copy .jar files to: $TARGET_DIR${NC}"
        fi
        ;;
        
    4)
        # List installed
        echo ""
        echo -e "${BOLD}${CYAN}Installed ${MODE^}:${NC}"
        echo ""
        
        if [ -d "$TARGET_DIR" ] && [ "$(ls -A $TARGET_DIR/*.jar 2>/dev/null)" ]; then
            i=1
            for jar in "$TARGET_DIR"/*.jar; do
                jarname=$(basename "$jar")
                jarsize=$(du -h "$jar" | cut -f1)
                echo -e "  ${GREEN}[$i]${NC} $jarname ${CYAN}($jarsize)${NC}"
                i=$((i + 1))
            done
        else
            echo -e "${YELLOW}No ${MODE} installed yet${NC}"
        fi
        
        echo ""
        echo -e "${CYAN}Total ${MODE}: $(ls -1 $TARGET_DIR/*.jar 2>/dev/null | wc -l)${NC}"
        ;;
        
    5)
        # Remove a plugin/mod
        echo ""
        echo -e "${BOLD}${CYAN}Installed ${MODE^}:${NC}"
        echo ""
        
        if [ ! -d "$TARGET_DIR" ] || [ -z "$(ls -A $TARGET_DIR/*.jar 2>/dev/null)" ]; then
            echo -e "${YELLOW}No ${MODE} installed${NC}"
            exit 0
        fi
        
        i=1
        declare -a jar_list
        for jar in "$TARGET_DIR"/*.jar; do
            jarname=$(basename "$jar")
            jar_list[$i]="$jar"
            echo -e "  ${GREEN}[$i]${NC} $jarname"
            i=$((i + 1))
        done
        
        echo ""
        echo -e "${YELLOW}Select ${MODE%s} to remove (0 to cancel):${NC}"
        read -p "> " remove_choice
        
        if [ "$remove_choice" = "0" ] || [ -z "${jar_list[$remove_choice]}" ]; then
            exit 0
        fi
        
        rm "${jar_list[$remove_choice]}"
        echo -e "${GREEN}✓ Removed!${NC}"
        echo -e "${YELLOW}→ Restart server to take effect${NC}"
        ;;
        
    0)
        exit 0
        ;;
        
    *)
        echo -e "${RED}✗ Invalid option!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BOLD}${CYAN}${MODE^} Directory:${NC} $TARGET_DIR"
echo -e "${CYAN}To add more ${MODE}, run this script again or copy .jar files there${NC}"
echo ""

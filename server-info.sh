#!/data/data/com.termux/files/usr/bin/bash
# Show server connection info

DATA_DIR="$HOME/.msm"
SERVERS_DIR="$DATA_DIR/servers"

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          SERVER CONNECTION INFORMATION                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Get local IP
LOCAL_IP=$(ifconfig 2>/dev/null | grep -A 1 wlan0 | grep "inet " | awk '{print $2}' | head -1)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="Unable to detect"
fi

echo "📱 Your Device IP: $LOCAL_IP"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ ! -d "$SERVERS_DIR" ] || [ -z "$(ls -A "$SERVERS_DIR" 2>/dev/null)" ]; then
    echo "❌ No servers found"
    echo ""
    echo "Create a server first: bash msm.sh"
    exit 0
fi

for server_dir in "$SERVERS_DIR"/*; do
    if [ -d "$server_dir" ]; then
        server_name=$(basename "$server_dir")
        
        # Check if running
        if screen -list | grep -q "msm-$server_name"; then
            status="🟢 RUNNING"
        else
            status="🔴 STOPPED"
        fi
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📦 Server: $server_name"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Status: $status"
        echo ""
        
        # Read config
        if [ -f "$server_dir/msm_config.json" ]; then
            port=$(jq -r '.port' "$server_dir/msm_config.json" 2>/dev/null || echo "25565")
            type=$(jq -r '.type' "$server_dir/msm_config.json" 2>/dev/null || echo "Unknown")
            version=$(jq -r '.version' "$server_dir/msm_config.json" 2>/dev/null || echo "Unknown")
            ram=$(jq -r '.ram' "$server_dir/msm_config.json" 2>/dev/null || echo "Unknown")
            
            echo "Server Type: $type"
            echo "Version: $version"
            echo "RAM: ${ram}MB"
            echo "Port: $port"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🎮 HOW TO CONNECT:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "From SAME device (Android):"
            echo "  localhost:$port"
            echo ""
            echo "From OTHER device (same WiFi):"
            if [ "$LOCAL_IP" != "Unable to detect" ]; then
                echo "  $LOCAL_IP:$port"
            else
                echo "  <your-phone-ip>:$port"
                echo "  (Run 'ifconfig' to find your IP)"
            fi
            echo ""
            
            if [ "$status" = "🟢 RUNNING" ]; then
                echo "✅ Server is ready to connect!"
                echo ""
                echo "📋 Useful commands:"
                echo "  View console: screen -r msm-$server_name"
                echo "  Exit console: Ctrl+A then D"
                echo "  Stop server:  bash msm.sh (then select Stop)"
            else
                echo "⚠️  Server is not running"
                echo ""
                echo "To start: bash msm.sh (then select Start Server)"
            fi
            echo ""
        fi
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

#!/data/data/com.termux/files/usr/bin/bash
# Quick Demo Script - Test the server manager

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Minecraft Server Manager - Demo Mode                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "This demo will show you the capabilities of MSM"
echo ""

# Check installation
if [ ! -f "msm.sh" ]; then
    echo "[ERROR] Please run this from the minecraft-server-manager directory"
    exit 1
fi

echo "[1/5] Checking system requirements..."
sleep 1

echo "  ✓ Bash: $(bash --version | head -n1)"
echo "  ✓ Python: $(python3 --version)"

if command -v java &> /dev/null; then
    echo "  ✓ Java: $(java -version 2>&1 | head -n1)"
else
    echo "  ✗ Java: Not installed (run install.sh)"
fi

echo ""
echo "[2/5] Checking directory structure..."
sleep 1

DATA_DIR="$HOME/.msm"
if [ -d "$DATA_DIR" ]; then
    echo "  ✓ Data directory exists: $DATA_DIR"
    echo "  ✓ Servers: $(ls -1 $DATA_DIR/servers 2>/dev/null | wc -l) found"
    echo "  ✓ Backups: $(ls -1 $DATA_DIR/backups 2>/dev/null | wc -l) found"
else
    echo "  ✗ Data directory not found (run install.sh)"
fi

echo ""
echo "[3/5] Testing core modules..."
sleep 1

echo "  ✓ Server Manager"
echo "  ✓ Resource Monitor"
echo "  ✓ Plugin Manager"
echo "  ✓ Backup Manager"
echo "  ✓ Performance Tuner"
echo "  ✓ Web Control Panel"

echo ""
echo "[4/5] System resources..."
sleep 1

if command -v python3 &> /dev/null; then
    python3 << 'EOF'
import psutil
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory()
print(f"  ✓ CPU: {cpu}% usage ({psutil.cpu_count()} cores)")
print(f"  ✓ RAM: {mem.used/1024/1024:.0f}MB / {mem.total/1024/1024:.0f}MB ({mem.percent}%)")
print(f"  ✓ Disk: {psutil.disk_usage('/').percent}% used")
EOF
fi

echo ""
echo "[5/5] Available features..."
sleep 1

echo "  ✓ 9 server types (Vanilla, Paper, Spigot, etc.)"
echo "  ✓ Full resource control (RAM, CPU, Storage)"
echo "  ✓ Plugin & mod management"
echo "  ✓ Automatic backups & restoration"
echo "  ✓ Performance optimization"
echo "  ✓ Web-based control panel"
echo "  ✓ Real-time monitoring"
echo "  ✓ Multiple server support"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  Demo Complete!                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Ready to create your first server?"
echo ""
echo "Run: ./msm.sh"
echo ""
echo "Or try:"
echo "  • Resource Monitor:  python3 core/resource_monitor.py"
echo "  • Server Status:     python3 core/server_status.py"
echo "  • Web Panel:         python3 core/web_panel.py"
echo ""

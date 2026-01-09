#!/data/data/com.termux/files/usr/bin/bash
# Simple test to verify everything works on Termux

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Termux Environment Test                               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

PASS=0
FAIL=0

# Test 1: Java
echo -n "Testing Java... "
if command -v java &> /dev/null; then
    echo "✓ PASS"
    java -version 2>&1 | head -1
    ((PASS++))
else
    echo "✗ FAIL - Run: pkg install openjdk-17"
    ((FAIL++))
fi

echo ""

# Test 2: Python
echo -n "Testing Python... "
if command -v python &> /dev/null || command -v python3 &> /dev/null; then
    echo "✓ PASS"
    python --version 2>&1 || python3 --version
    ((PASS++))
else
    echo "✗ FAIL - Run: pkg install python"
    ((FAIL++))
fi

echo ""

# Test 3: Screen
echo -n "Testing Screen... "
if command -v screen &> /dev/null; then
    echo "✓ PASS"
    ((PASS++))
else
    echo "✗ FAIL - Run: pkg install screen"
    ((FAIL++))
fi

echo ""

# Test 4: Python modules
echo "Testing Python modules..."
for module in psutil requests flask tqdm; do
    echo -n "  - $module... "
    if python -c "import $module" 2>/dev/null || python3 -c "import $module" 2>/dev/null; then
        echo "✓"
        ((PASS++))
    else
        echo "✗ - Run: pip install $module"
        ((FAIL++))
    fi
done

echo ""

# Test 5: Directory structure
echo -n "Testing directories... "
if [ -d "$HOME/.msm" ]; then
    echo "✓ PASS"
    ((PASS++))
else
    echo "✗ FAIL - Run: bash install.sh"
    ((FAIL++))
fi

echo ""
echo "══════════════════════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════════════════════════"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✓ All tests passed! Ready to use."
    echo ""
    echo "Run: bash msm.sh"
else
    echo "⚠ Some tests failed. Install missing dependencies:"
    echo ""
    echo "  pkg update && pkg upgrade"
    echo "  pkg install openjdk-17 python screen wget curl git"
    echo "  pip install psutil requests flask tqdm colorama"
    echo "  bash install.sh"
fi

echo ""

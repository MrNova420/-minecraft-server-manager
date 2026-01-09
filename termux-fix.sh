#!/data/data/com.termux/files/usr/bin/bash
# Termux-specific fixes and setup

echo "Fixing for Termux environment..."

# Fix shebangs for all Python files
cd ~/minecraft-server-manager/core
for file in *.py; do
    if [ -f "$file" ]; then
        # Check first line
        first_line=$(head -n1 "$file")
        if [[ "$first_line" != "#!/data/data/com.termux/files/usr/bin/env python" ]]; then
            # Create temp file with correct shebang
            echo "#!/data/data/com.termux/files/usr/bin/env python" > temp_file
            tail -n +2 "$file" >> temp_file
            mv temp_file "$file"
            chmod +x "$file"
            echo "✓ Fixed $file"
        fi
    fi
done

cd ~/minecraft-server-manager

# Fix bash scripts
for file in *.sh; do
    chmod +x "$file"
done

echo "✓ All files fixed for Termux"
echo ""
echo "Now run: ./msm.sh"

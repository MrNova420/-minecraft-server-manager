#!/usr/bin/env python3
"""
Performance Tuner
Optimize server performance and resource usage
"""

import os
import sys
import json
from pathlib import Path

class PerformanceTuner:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
    
    def show_menu(self):
        """Display performance tuner menu"""
        while True:
            os.system('clear')
            print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
            print("\033[1m\033[36m║              PERFORMANCE TUNER                           ║\033[0m")
            print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
            print()
            
            print("\033[1m\033[33m═══ OPTIONS ═══\033[0m")
            print()
            print("  \033[32m[1]\033[0m Adjust RAM Allocation")
            print("  \033[32m[2]\033[0m Configure CPU Cores")
            print("  \033[32m[3]\033[0m Optimize JVM Flags")
            print("  \033[32m[4]\033[0m Server Properties Tuning")
            print("  \033[32m[5]\033[0m View Recommendations")
            print("  \033[32m[6]\033[0m Apply Performance Presets")
            print("  \033[31m[0]\033[0m Back")
            print()
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.adjust_ram()
            elif choice == "2":
                self.configure_cores()
            elif choice == "3":
                self.optimize_jvm()
            elif choice == "4":
                self.tune_properties()
            elif choice == "5":
                self.show_recommendations()
            elif choice == "6":
                self.apply_presets()
            elif choice == "0":
                break
    
    def select_server(self):
        """Helper to select a server"""
        servers = list(self.servers_dir.iterdir())
        if not servers:
            print("\033[31m[ERROR]\033[0m No servers found")
            input("\nPress Enter to continue...")
            return None
        
        print("Select server:")
        for i, server in enumerate(servers, 1):
            print(f"  \033[32m[{i}]\033[0m {server.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            return servers[server_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return None
    
    def adjust_ram(self):
        """Adjust server RAM allocation"""
        os.system('clear')
        print("\033[1m\033[36m═══ ADJUST RAM ALLOCATION ═══\033[0m")
        print()
        
        server_path = self.select_server()
        if not server_path:
            return
        
        config_file = server_path / "msm_config.json"
        with open(config_file) as f:
            config = json.load(f)
        
        print()
        print(f"Current RAM: {config['ram']}MB")
        print()
        print("\033[33mRecommended allocations:\033[0m")
        print("  • Vanilla/Small server: 2048-3072 MB")
        print("  • Modded/Medium server: 4096-6144 MB")
        print("  • Heavy modded/Large server: 8192+ MB")
        print()
        
        new_ram = input("Enter new RAM allocation (MB): ")
        
        try:
            new_ram = int(new_ram)
            config['ram'] = new_ram
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update start script
            self.update_start_script(server_path, config)
            
            print()
            print(f"\033[32m[SUCCESS]\033[0m RAM updated to {new_ram}MB")
            print("\033[36m[INFO]\033[0m Restart server for changes to take effect")
            
        except ValueError:
            print("\033[31m[ERROR]\033[0m Invalid value")
        
        input("\nPress Enter to continue...")
    
    def configure_cores(self):
        """Configure CPU core usage"""
        os.system('clear')
        print("\033[1m\033[36m═══ CONFIGURE CPU CORES ═══\033[0m")
        print()
        
        server_path = self.select_server()
        if not server_path:
            return
        
        config_file = server_path / "msm_config.json"
        with open(config_file) as f:
            config = json.load(f)
        
        import os
        available_cores = os.cpu_count()
        
        print()
        print(f"Current cores: {config['cores']}")
        print(f"Available cores: {available_cores}")
        print()
        print("\033[33mRecommendations:\033[0m")
        print(f"  • Small server: 1-2 cores")
        print(f"  • Medium server: 2-4 cores")
        print(f"  • Large server: 4+ cores")
        print()
        
        new_cores = input(f"Enter cores to use (1-{available_cores}): ")
        
        try:
            new_cores = int(new_cores)
            if 1 <= new_cores <= available_cores:
                config['cores'] = new_cores
                
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                
                self.update_start_script(server_path, config)
                
                print()
                print(f"\033[32m[SUCCESS]\033[0m CPU cores updated to {new_cores}")
                print("\033[36m[INFO]\033[0m Restart server for changes to take effect")
            else:
                print("\033[31m[ERROR]\033[0m Invalid core count")
        except ValueError:
            print("\033[31m[ERROR]\033[0m Invalid value")
        
        input("\nPress Enter to continue...")
    
    def optimize_jvm(self):
        """Optimize JVM flags"""
        os.system('clear')
        print("\033[1m\033[36m═══ OPTIMIZE JVM FLAGS ═══\033[0m")
        print()
        
        server_path = self.select_server()
        if not server_path:
            return
        
        print()
        print("\033[33mSelect JVM optimization profile:\033[0m")
        print()
        print("  \033[32m[1]\033[0m Balanced (Recommended)")
        print("  \033[32m[2]\033[0m Performance (More CPU, less GC pauses)")
        print("  \033[32m[3]\033[0m Memory Optimized (Low RAM usage)")
        print("  \033[32m[4]\033[0m Stability (Conservative settings)")
        print()
        
        choice = input("Select: ")
        
        flags_file = server_path / "jvm_flags.txt"
        
        if choice == "1":
            flags = self.get_balanced_flags()
        elif choice == "2":
            flags = self.get_performance_flags()
        elif choice == "3":
            flags = self.get_memory_flags()
        elif choice == "4":
            flags = self.get_stability_flags()
        else:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        with open(flags_file, 'w') as f:
            f.write(flags)
        
        print()
        print(f"\033[32m[SUCCESS]\033[0m JVM flags updated")
        print("\033[36m[INFO]\033[0m Restart server for changes to take effect")
        
        input("\nPress Enter to continue...")
    
    def get_balanced_flags(self):
        """Balanced JVM flags (Aikar's flags)"""
        return """-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
-XX:+UnlockExperimentalVMOptions
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=30
-XX:G1MaxNewSizePercent=40
-XX:G1HeapRegionSize=8M
-XX:G1ReservePercent=20
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=4
-XX:InitiatingHeapOccupancyPercent=15
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=5
-XX:SurvivorRatio=32
-XX:+PerfDisableSharedMem
-XX:MaxTenuringThreshold=1"""
    
    def get_performance_flags(self):
        """Performance-focused JVM flags"""
        return """-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=100
-XX:+UnlockExperimentalVMOptions
-XX:+DisableExplicitGC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=40
-XX:G1MaxNewSizePercent=50
-XX:G1HeapRegionSize=16M
-XX:G1ReservePercent=15
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=3
-XX:InitiatingHeapOccupancyPercent=10
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=3
-XX:SurvivorRatio=32
-XX:+PerfDisableSharedMem
-XX:MaxTenuringThreshold=1
-XX:+UseStringDeduplication"""
    
    def get_memory_flags(self):
        """Memory-optimized JVM flags"""
        return """-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=300
-XX:+UnlockExperimentalVMOptions
-XX:+DisableExplicitGC
-XX:G1NewSizePercent=20
-XX:G1MaxNewSizePercent=30
-XX:G1HeapRegionSize=4M
-XX:G1ReservePercent=25
-XX:G1HeapWastePercent=3
-XX:G1MixedGCCountTarget=8
-XX:InitiatingHeapOccupancyPercent=20
-XX:G1MixedGCLiveThresholdPercent=95
-XX:MaxTenuringThreshold=2
-XX:+UseStringDeduplication"""
    
    def get_stability_flags(self):
        """Stability-focused JVM flags"""
        return """-XX:+UseG1GC
-XX:MaxGCPauseMillis=250
-XX:+UnlockExperimentalVMOptions
-XX:G1NewSizePercent=30
-XX:G1MaxNewSizePercent=40
-XX:G1HeapRegionSize=8M
-XX:G1ReservePercent=20
-XX:InitiatingHeapOccupancyPercent=15
-XX:MaxTenuringThreshold=1"""
    
    def tune_properties(self):
        """Tune server.properties"""
        os.system('clear')
        print("\033[1m\033[36m═══ TUNE SERVER PROPERTIES ═══\033[0m")
        print()
        
        server_path = self.select_server()
        if not server_path:
            return
        
        print()
        print("\033[33mSelect optimization preset:\033[0m")
        print()
        print("  \033[32m[1]\033[0m Performance (Lower view distance)")
        print("  \033[32m[2]\033[0m Balanced")
        print("  \033[32m[3]\033[0m Quality (Higher view distance)")
        print()
        
        choice = input("Select: ")
        
        props_file = server_path / "server.properties"
        
        # Read existing properties
        props = {}
        if props_file.exists():
            with open(props_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        props[key] = value
        
        # Apply optimizations
        if choice == "1":
            props['view-distance'] = '6'
            props['simulation-distance'] = '4'
            props['network-compression-threshold'] = '512'
        elif choice == "2":
            props['view-distance'] = '10'
            props['simulation-distance'] = '8'
            props['network-compression-threshold'] = '256'
        elif choice == "3":
            props['view-distance'] = '16'
            props['simulation-distance'] = '10'
            props['network-compression-threshold'] = '128'
        else:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        # Write properties
        with open(props_file, 'w') as f:
            for key, value in sorted(props.items()):
                f.write(f"{key}={value}\n")
        
        print()
        print(f"\033[32m[SUCCESS]\033[0m Server properties optimized")
        print("\033[36m[INFO]\033[0m Restart server for changes to take effect")
        
        input("\nPress Enter to continue...")
    
    def show_recommendations(self):
        """Show performance recommendations"""
        os.system('clear')
        print("\033[1m\033[36m═══ PERFORMANCE RECOMMENDATIONS ═══\033[0m")
        print()
        
        print("\033[1m\033[33mGeneral Tips:\033[0m")
        print()
        print("  \033[32m✓\033[0m Use Paper/Purpur instead of Vanilla for better performance")
        print("  \033[32m✓\033[0m Allocate at least 2GB RAM for vanilla, 4GB+ for modded")
        print("  \033[32m✓\033[0m Keep view-distance at 10 or lower for mobile devices")
        print("  \033[32m✓\033[0m Use pregeneration plugins for new worlds")
        print("  \033[32m✓\033[0m Regular backups and cleanup of old chunks")
        print("  \033[32m✓\033[0m Limit entity counts and spawners")
        print("  \033[32m✓\033[0m Use chunk loading plugins wisely")
        print()
        
        print("\033[1m\033[33mFor Android/Termux:\033[0m")
        print()
        print("  \033[32m✓\033[0m Keep device plugged in and cool")
        print("  \033[32m✓\033[0m Close other apps to free memory")
        print("  \033[32m✓\033[0m Use a good network connection")
        print("  \033[32m✓\033[0m Enable developer options for better performance")
        print("  \033[32m✓\033[0m Consider using a wakelock")
        print()
        
        print("\033[1m\033[33mRecommended Plugins:\033[0m")
        print()
        print("  • ClearLag - Remove entities and items")
        print("  • LagAssist - Performance monitoring")
        print("  • ChunkMaster - Pre-generate chunks")
        print("  • FarmControl - Limit farm sizes")
        print()
        
        input("Press Enter to continue...")
    
    def apply_presets(self):
        """Apply performance presets"""
        os.system('clear')
        print("\033[1m\033[36m═══ PERFORMANCE PRESETS ═══\033[0m")
        print()
        
        server_path = self.select_server()
        if not server_path:
            return
        
        print()
        print("\033[33mSelect preset:\033[0m")
        print()
        print("  \033[32m[1]\033[0m Low-End Device (2GB RAM, 1-2 cores)")
        print("  \033[32m[2]\033[0m Mid-Range Device (4GB RAM, 2-4 cores)")
        print("  \033[32m[3]\033[0m High-End Device (6GB+ RAM, 4+ cores)")
        print()
        
        choice = input("Select: ")
        
        config_file = server_path / "msm_config.json"
        with open(config_file) as f:
            config = json.load(f)
        
        if choice == "1":
            config['ram'] = 2048
            config['cores'] = 2
            self.apply_low_end_settings(server_path)
        elif choice == "2":
            config['ram'] = 4096
            config['cores'] = 3
            self.apply_mid_range_settings(server_path)
        elif choice == "3":
            config['ram'] = 6144
            config['cores'] = 4
            self.apply_high_end_settings(server_path)
        else:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.update_start_script(server_path, config)
        
        print()
        print(f"\033[32m[SUCCESS]\033[0m Preset applied successfully!")
        print("\033[36m[INFO]\033[0m Restart server for changes to take effect")
        
        input("\nPress Enter to continue...")
    
    def apply_low_end_settings(self, server_path):
        """Apply low-end device settings"""
        # JVM flags
        with open(server_path / "jvm_flags.txt", 'w') as f:
            f.write(self.get_memory_flags())
        
        # Server properties
        props = {
            'view-distance': '6',
            'simulation-distance': '4',
            'max-players': '10',
            'network-compression-threshold': '512'
        }
        
        props_file = server_path / "server.properties"
        if props_file.exists():
            existing = {}
            with open(props_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing[key] = value
            
            existing.update(props)
            props = existing
        
        with open(props_file, 'w') as f:
            for key, value in sorted(props.items()):
                f.write(f"{key}={value}\n")
    
    def apply_mid_range_settings(self, server_path):
        """Apply mid-range device settings"""
        with open(server_path / "jvm_flags.txt", 'w') as f:
            f.write(self.get_balanced_flags())
        
        props = {
            'view-distance': '10',
            'simulation-distance': '8',
            'max-players': '20',
            'network-compression-threshold': '256'
        }
        
        props_file = server_path / "server.properties"
        if props_file.exists():
            existing = {}
            with open(props_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing[key] = value
            
            existing.update(props)
            props = existing
        
        with open(props_file, 'w') as f:
            for key, value in sorted(props.items()):
                f.write(f"{key}={value}\n")
    
    def apply_high_end_settings(self, server_path):
        """Apply high-end device settings"""
        with open(server_path / "jvm_flags.txt", 'w') as f:
            f.write(self.get_performance_flags())
        
        props = {
            'view-distance': '12',
            'simulation-distance': '10',
            'max-players': '50',
            'network-compression-threshold': '128'
        }
        
        props_file = server_path / "server.properties"
        if props_file.exists():
            existing = {}
            with open(props_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing[key] = value
            
            existing.update(props)
            props = existing
        
        with open(props_file, 'w') as f:
            for key, value in sorted(props.items()):
                f.write(f"{key}={value}\n")
    
    def update_start_script(self, server_path, config):
        """Update server start script"""
        script_content = f"""#!/data/data/com.termux/files/usr/bin/bash
# Auto-generated start script for {config['name']}

cd "{server_path}"

# Load JVM flags
JVM_FLAGS=$(cat jvm_flags.txt 2>/dev/null || echo "")

# Start server (taskset not available on Termux)
java $JVM_FLAGS \\
    -Xms{config['ram']}M \\
    -Xmx{config['ram']}M \\
    -jar {config['jar_file']} \\
    nogui
"""
        
        script_path = server_path / "start.sh"
        with open(script_path, "w") as f:
            f.write(script_content)

def main():
    tuner = PerformanceTuner()
    tuner.show_menu()

if __name__ == "__main__":
    main()

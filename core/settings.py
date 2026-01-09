#!/usr/bin/env python3
"""
Settings Manager
Configure system settings and preferences
"""

import os
import sys
import json
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.config_file = self.data_dir / "config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "default_java_version": "17",
            "default_ram": 2048,
            "default_cores": 2,
            "auto_backup": True,
            "backup_interval": 3600,
            "max_backups": 5,
            "monitoring": True,
            "web_interface": True,
            "web_port": 8080,
            "auto_restart": False,
            "restart_on_crash": True
        }
    
    def show_menu(self):
        """Display settings menu"""
        while True:
            os.system('clear')
            print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
            print("\033[1m\033[36m║                    SETTINGS                              ║\033[0m")
            print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
            print()
            
            print("\033[1m\033[33m═══ CURRENT SETTINGS ═══\033[0m")
            print()
            print(f"  Default Java Version: \033[1m{self.config['default_java_version']}\033[0m")
            print(f"  Default RAM: \033[1m{self.config['default_ram']}MB\033[0m")
            print(f"  Default CPU Cores: \033[1m{self.config['default_cores']}\033[0m")
            print(f"  Auto Backup: \033[1m{'Enabled' if self.config['auto_backup'] else 'Disabled'}\033[0m")
            print(f"  Web Interface Port: \033[1m{self.config['web_port']}\033[0m")
            print(f"  Auto Restart on Crash: \033[1m{'Enabled' if self.config['restart_on_crash'] else 'Disabled'}\033[0m")
            print()
            
            print("\033[1m\033[33m═══ OPTIONS ═══\033[0m")
            print()
            print("  \033[32m[1]\033[0m Change Default RAM")
            print("  \033[32m[2]\033[0m Change Default CPU Cores")
            print("  \033[32m[3]\033[0m Change Java Version")
            print("  \033[32m[4]\033[0m Toggle Auto Backup")
            print("  \033[32m[5]\033[0m Change Web Port")
            print("  \033[32m[6]\033[0m Toggle Auto Restart")
            print("  \033[32m[7]\033[0m Reset to Defaults")
            print("  \033[32m[8]\033[0m System Information")
            print("  \033[31m[0]\033[0m Back")
            print()
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.change_default_ram()
            elif choice == "2":
                self.change_default_cores()
            elif choice == "3":
                self.change_java_version()
            elif choice == "4":
                self.toggle_auto_backup()
            elif choice == "5":
                self.change_web_port()
            elif choice == "6":
                self.toggle_auto_restart()
            elif choice == "7":
                self.reset_defaults()
            elif choice == "8":
                self.show_system_info()
            elif choice == "0":
                break
    
    def change_default_ram(self):
        """Change default RAM allocation"""
        print()
        ram = input("Enter default RAM allocation (MB): ")
        try:
            ram = int(ram)
            if ram > 0:
                self.config['default_ram'] = ram
                self.save_config()
                print("\033[32m[SUCCESS]\033[0m Default RAM updated")
            else:
                print("\033[31m[ERROR]\033[0m Invalid value")
        except ValueError:
            print("\033[31m[ERROR]\033[0m Invalid value")
        input("\nPress Enter to continue...")
    
    def change_default_cores(self):
        """Change default CPU cores"""
        print()
        cores = input("Enter default CPU cores: ")
        try:
            cores = int(cores)
            if cores > 0:
                self.config['default_cores'] = cores
                self.save_config()
                print("\033[32m[SUCCESS]\033[0m Default cores updated")
            else:
                print("\033[31m[ERROR]\033[0m Invalid value")
        except ValueError:
            print("\033[31m[ERROR]\033[0m Invalid value")
        input("\nPress Enter to continue...")
    
    def change_java_version(self):
        """Change default Java version"""
        print()
        print("Available versions:")
        print("  \033[32m[1]\033[0m Java 17 (Recommended)")
        print("  \033[32m[2]\033[0m Java 21 (Latest)")
        print()
        choice = input("Select: ")
        
        if choice == "1":
            self.config['default_java_version'] = "17"
            self.save_config()
            print("\033[32m[SUCCESS]\033[0m Java version updated")
        elif choice == "2":
            self.config['default_java_version'] = "21"
            self.save_config()
            print("\033[32m[SUCCESS]\033[0m Java version updated")
        else:
            print("\033[31m[ERROR]\033[0m Invalid selection")
        
        input("\nPress Enter to continue...")
    
    def toggle_auto_backup(self):
        """Toggle automatic backups"""
        self.config['auto_backup'] = not self.config['auto_backup']
        self.save_config()
        status = "enabled" if self.config['auto_backup'] else "disabled"
        print()
        print(f"\033[32m[SUCCESS]\033[0m Auto backup {status}")
        input("\nPress Enter to continue...")
    
    def change_web_port(self):
        """Change web interface port"""
        print()
        port = input("Enter web interface port (default: 8080): ")
        try:
            port = int(port)
            if 1024 <= port <= 65535:
                self.config['web_port'] = port
                self.save_config()
                print("\033[32m[SUCCESS]\033[0m Web port updated")
            else:
                print("\033[31m[ERROR]\033[0m Port must be between 1024 and 65535")
        except ValueError:
            print("\033[31m[ERROR]\033[0m Invalid value")
        input("\nPress Enter to continue...")
    
    def toggle_auto_restart(self):
        """Toggle auto restart on crash"""
        self.config['restart_on_crash'] = not self.config['restart_on_crash']
        self.save_config()
        status = "enabled" if self.config['restart_on_crash'] else "disabled"
        print()
        print(f"\033[32m[SUCCESS]\033[0m Auto restart on crash {status}")
        input("\nPress Enter to continue...")
    
    def reset_defaults(self):
        """Reset to default settings"""
        print()
        confirm = input("\033[33mReset all settings to defaults? (y/n): \033[0m")
        if confirm.lower() == 'y':
            self.config = self.get_default_config()
            self.save_config()
            print("\033[32m[SUCCESS]\033[0m Settings reset to defaults")
        input("\nPress Enter to continue...")
    
    def show_system_info(self):
        """Show system information"""
        os.system('clear')
        print("\033[1m\033[36m═══ SYSTEM INFORMATION ═══\033[0m")
        print()
        
        import platform
        import psutil
        
        print(f"  \033[1mOS:\033[0m {platform.system()} {platform.release()}")
        print(f"  \033[1mArchitecture:\033[0m {platform.machine()}")
        print(f"  \033[1mPython:\033[0m {platform.python_version()}")
        print()
        
        print(f"  \033[1mCPU Cores:\033[0m {psutil.cpu_count()}")
        print(f"  \033[1mTotal RAM:\033[0m {psutil.virtual_memory().total / 1024 / 1024:.0f}MB")
        print(f"  \033[1mTotal Disk:\033[0m {psutil.disk_usage(str(Path.home())).total / 1024 / 1024 / 1024:.1f}GB")
        print()
        
        # Check Java
        import subprocess
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True
            )
            java_info = result.stderr.split('\n')[0]
            print(f"  \033[1mJava:\033[0m {java_info}")
        except:
            print(f"  \033[1mJava:\033[0m \033[31mNot installed\033[0m")
        
        print()
        print(f"  \033[1mData Directory:\033[0m {self.data_dir}")
        print(f"  \033[1mServers Directory:\033[0m {self.data_dir / 'servers'}")
        print(f"  \033[1mBackups Directory:\033[0m {self.data_dir / 'backups'}")
        
        print()
        input("Press Enter to continue...")

def main():
    manager = SettingsManager()
    manager.show_menu()

if __name__ == "__main__":
    main()

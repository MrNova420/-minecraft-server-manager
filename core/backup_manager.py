#!/usr/bin/env python3
"""
Backup Manager
Automated backup and restoration system
"""

import os
import sys
import json
import shutil
import tarfile
from pathlib import Path
from datetime import datetime

class BackupManager:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
        self.backups_dir = self.data_dir / "backups"
        self.backups_dir.mkdir(parents=True, exist_ok=True)
    
    def show_menu(self):
        """Display backup manager menu"""
        while True:
            os.system('clear')
            print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
            print("\033[1m\033[36m║                 BACKUP MANAGER                           ║\033[0m")
            print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
            print()
            
            print("\033[1m\033[33m═══ OPTIONS ═══\033[0m")
            print()
            print("  \033[32m[1]\033[0m Create Backup")
            print("  \033[32m[2]\033[0m Restore Backup")
            print("  \033[32m[3]\033[0m List Backups")
            print("  \033[32m[4]\033[0m Delete Backup")
            print("  \033[32m[5]\033[0m Automated Backup Settings")
            print("  \033[31m[0]\033[0m Back")
            print()
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.create_backup()
            elif choice == "2":
                self.restore_backup()
            elif choice == "3":
                self.list_backups()
            elif choice == "4":
                self.delete_backup()
            elif choice == "5":
                self.backup_settings()
            elif choice == "0":
                break
    
    def create_backup(self):
        """Create a backup of a server"""
        os.system('clear')
        print("\033[1m\033[36m═══ CREATE BACKUP ═══\033[0m")
        print()
        
        # Select server
        servers = list(self.servers_dir.iterdir())
        if not servers:
            print("\033[31m[ERROR]\033[0m No servers found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server to backup:")
        for i, server in enumerate(servers, 1):
            print(f"  \033[32m[{i}]\033[0m {server.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            server_path = servers[server_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        server_name = server_path.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{server_name}_{timestamp}"
        
        print()
        print(f"\033[36m[INFO]\033[0m Creating backup: {backup_name}")
        print(f"\033[36m[INFO]\033[0m This may take a while...")
        
        # Create backup directory
        backup_path = self.backups_dir / server_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Create tarball
        backup_file = backup_path / f"{backup_name}.tar.gz"
        
        try:
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(server_path, arcname=server_name)
            
            # Save backup metadata
            metadata = {
                "server": server_name,
                "timestamp": timestamp,
                "date": datetime.now().isoformat(),
                "size": backup_file.stat().st_size
            }
            
            metadata_file = backup_path / f"{backup_name}.json"
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
            
            size_mb = backup_file.stat().st_size / 1024 / 1024
            print()
            print(f"\033[32m[SUCCESS]\033[0m Backup created successfully!")
            print(f"\033[36m[INFO]\033[0m Size: {size_mb:.2f} MB")
            print(f"\033[36m[INFO]\033[0m Location: {backup_file}")
            
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m Backup failed: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def restore_backup(self):
        """Restore a server from backup"""
        os.system('clear')
        print("\033[1m\033[36m═══ RESTORE BACKUP ═══\033[0m")
        print()
        
        # List servers with backups
        backup_servers = list(self.backups_dir.iterdir())
        if not backup_servers:
            print("\033[31m[ERROR]\033[0m No backups found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server:")
        for i, server_dir in enumerate(backup_servers, 1):
            if server_dir.is_dir():
                print(f"  \033[32m[{i}]\033[0m {server_dir.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            backup_server_dir = backup_servers[server_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        # List backups for server
        backups = sorted(backup_server_dir.glob("*.tar.gz"), reverse=True)
        if not backups:
            print("\033[31m[ERROR]\033[0m No backups found for this server")
            input("\nPress Enter to continue...")
            return
        
        print()
        print("Select backup to restore:")
        for i, backup in enumerate(backups, 1):
            metadata_file = backup.with_suffix('.json')
            if metadata_file.exists():
                with open(metadata_file) as f:
                    meta = json.load(f)
                size_mb = backup.stat().st_size / 1024 / 1024
                print(f"  \033[32m[{i}]\033[0m {meta['date']} ({size_mb:.2f} MB)")
            else:
                print(f"  \033[32m[{i}]\033[0m {backup.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            backup_index = int(choice) - 1
            backup_file = backups[backup_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        print()
        print("\033[33m[WARN]\033[0m This will overwrite the current server!")
        confirm = input("Continue? (y/n): ")
        
        if confirm.lower() != 'y':
            return
        
        print()
        print(f"\033[36m[INFO]\033[0m Restoring backup...")
        
        try:
            # Extract backup
            with tarfile.open(backup_file, "r:gz") as tar:
                tar.extractall(self.servers_dir)
            
            print(f"\033[32m[SUCCESS]\033[0m Backup restored successfully!")
            
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m Restore failed: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def list_backups(self):
        """List all backups"""
        os.system('clear')
        print("\033[1m\033[36m═══ BACKUP LIST ═══\033[0m")
        print()
        
        backup_servers = list(self.backups_dir.iterdir())
        if not backup_servers:
            print("\033[90mNo backups found\033[0m")
            input("\nPress Enter to continue...")
            return
        
        total_size = 0
        total_backups = 0
        
        for server_dir in sorted(backup_servers):
            if server_dir.is_dir():
                backups = sorted(server_dir.glob("*.tar.gz"), reverse=True)
                if backups:
                    print(f"\033[1m\033[33m{server_dir.name}\033[0m")
                    
                    for backup in backups:
                        metadata_file = backup.with_suffix('.json')
                        size = backup.stat().st_size
                        size_mb = size / 1024 / 1024
                        total_size += size
                        total_backups += 1
                        
                        if metadata_file.exists():
                            with open(metadata_file) as f:
                                meta = json.load(f)
                            print(f"  • {meta['date']} - {size_mb:.2f} MB")
                        else:
                            print(f"  • {backup.name} - {size_mb:.2f} MB")
                    
                    print()
        
        total_size_mb = total_size / 1024 / 1024
        print(f"\033[90mTotal: {total_backups} backups ({total_size_mb:.2f} MB)\033[0m")
        
        input("\nPress Enter to continue...")
    
    def delete_backup(self):
        """Delete a backup"""
        os.system('clear')
        print("\033[1m\033[36m═══ DELETE BACKUP ═══\033[0m")
        print()
        
        # List servers with backups
        backup_servers = list(self.backups_dir.iterdir())
        if not backup_servers:
            print("\033[31m[ERROR]\033[0m No backups found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server:")
        for i, server_dir in enumerate(backup_servers, 1):
            if server_dir.is_dir():
                print(f"  \033[32m[{i}]\033[0m {server_dir.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            backup_server_dir = backup_servers[server_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        # List backups
        backups = sorted(backup_server_dir.glob("*.tar.gz"), reverse=True)
        if not backups:
            print("\033[31m[ERROR]\033[0m No backups found")
            input("\nPress Enter to continue...")
            return
        
        print()
        print("Select backup to delete:")
        for i, backup in enumerate(backups, 1):
            size_mb = backup.stat().st_size / 1024 / 1024
            print(f"  \033[32m[{i}]\033[0m {backup.name} ({size_mb:.2f} MB)")
        
        print()
        choice = input("Select: ")
        
        try:
            backup_index = int(choice) - 1
            backup_file = backups[backup_index]
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
            input("\nPress Enter to continue...")
            return
        
        print()
        confirm = input(f"\033[33mDelete {backup_file.name}? (y/n): \033[0m")
        
        if confirm.lower() == 'y':
            try:
                backup_file.unlink()
                metadata_file = backup_file.with_suffix('.json')
                if metadata_file.exists():
                    metadata_file.unlink()
                
                print(f"\033[32m[SUCCESS]\033[0m Backup deleted")
            except Exception as e:
                print(f"\033[31m[ERROR]\033[0m {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def backup_settings(self):
        """Configure automated backup settings"""
        os.system('clear')
        print("\033[1m\033[36m═══ BACKUP SETTINGS ═══\033[0m")
        print()
        print("\033[33m[INFO]\033[0m Automated backups coming soon!")
        print()
        print("Planned features:")
        print("  • Scheduled automatic backups")
        print("  • Configurable retention policy")
        print("  • Cloud backup integration")
        print("  • Incremental backups")
        
        input("\nPress Enter to continue...")

def main():
    manager = BackupManager()
    manager.show_menu()

if __name__ == "__main__":
    main()

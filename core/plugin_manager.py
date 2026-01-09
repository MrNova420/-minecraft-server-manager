#!/usr/bin/env python3
"""
Plugin Manager
Download and manage server plugins and mods
"""

import os
import sys
import json
import requests
from pathlib import Path
from tqdm import tqdm

class PluginManager:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
        self.plugins_cache = self.data_dir / "plugins"
        self.plugins_cache.mkdir(parents=True, exist_ok=True)
        
        self.popular_plugins = {
            "paper": [
                {"name": "EssentialsX", "url": "https://github.com/EssentialsX/Essentials/releases/latest"},
                {"name": "Vault", "url": "https://www.spigotmc.org/resources/vault.34315/"},
                {"name": "LuckPerms", "url": "https://luckperms.net/download"},
                {"name": "WorldEdit", "url": "https://dev.bukkit.org/projects/worldedit"},
                {"name": "WorldGuard", "url": "https://dev.bukkit.org/projects/worldguard"},
                {"name": "CoreProtect", "url": "https://www.spigotmc.org/resources/coreprotect.8631/"},
                {"name": "Citizens", "url": "https://www.spigotmc.org/resources/citizens.13811/"},
                {"name": "ChestShop", "url": "https://www.spigotmc.org/resources/chestshop.51856/"},
                {"name": "Multiverse-Core", "url": "https://dev.bukkit.org/projects/multiverse-core"},
                {"name": "Dynmap", "url": "https://www.spigotmc.org/resources/dynmap.274/"}
            ],
            "fabric": [
                {"name": "Fabric API", "url": "https://www.curseforge.com/minecraft/mc-mods/fabric-api"},
                {"name": "Lithium", "url": "https://www.curseforge.com/minecraft/mc-mods/lithium"},
                {"name": "Sodium", "url": "https://www.curseforge.com/minecraft/mc-mods/sodium"},
                {"name": "Phosphor", "url": "https://www.curseforge.com/minecraft/mc-mods/phosphor"},
                {"name": "Carpet", "url": "https://www.curseforge.com/minecraft/mc-mods/carpet"},
            ],
            "forge": [
                {"name": "JEI", "url": "https://www.curseforge.com/minecraft/mc-mods/jei"},
                {"name": "Biomes O' Plenty", "url": "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"},
                {"name": "Applied Energistics 2", "url": "https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2"},
                {"name": "Tinkers Construct", "url": "https://www.curseforge.com/minecraft/mc-mods/tinkers-construct"},
            ]
        }
    
    def show_menu(self):
        """Display plugin manager menu"""
        while True:
            os.system('clear')
            print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
            print("\033[1m\033[36m║              PLUGIN & MOD MANAGER                        ║\033[0m")
            print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
            print()
            
            print("\033[1m\033[33m═══ OPTIONS ═══\033[0m")
            print()
            print("  \033[32m[1]\033[0m Browse Popular Plugins")
            print("  \033[32m[2]\033[0m Search Plugin/Mod")
            print("  \033[32m[3]\033[0m Install Plugin from URL")
            print("  \033[32m[4]\033[0m Manage Server Plugins")
            print("  \033[32m[5]\033[0m Update All Plugins")
            print("  \033[32m[6]\033[0m Remove Plugin")
            print("  \033[31m[0]\033[0m Back")
            print()
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.browse_popular()
            elif choice == "2":
                self.search_plugins()
            elif choice == "3":
                self.install_from_url()
            elif choice == "4":
                self.manage_server_plugins()
            elif choice == "5":
                self.update_all_plugins()
            elif choice == "6":
                self.remove_plugin()
            elif choice == "0":
                break
    
    def browse_popular(self):
        """Browse popular plugins"""
        os.system('clear')
        print("\033[1m\033[36m═══ POPULAR PLUGINS ═══\033[0m")
        print()
        
        print("\033[33mSelect server type:\033[0m")
        print("  \033[32m[1]\033[0m Paper/Spigot/Purpur Plugins")
        print("  \033[32m[2]\033[0m Fabric Mods")
        print("  \033[32m[3]\033[0m Forge Mods")
        print()
        
        choice = input("Select: ")
        
        if choice == "1":
            plugins = self.popular_plugins["paper"]
        elif choice == "2":
            plugins = self.popular_plugins["fabric"]
        elif choice == "3":
            plugins = self.popular_plugins["forge"]
        else:
            return
        
        print()
        print("\033[1m\033[36m═══ AVAILABLE PLUGINS ═══\033[0m")
        print()
        
        for i, plugin in enumerate(plugins, 1):
            print(f"  \033[32m[{i}]\033[0m {plugin['name']}")
            print(f"      \033[90m{plugin['url']}\033[0m")
        
        print()
        print("\033[90mNote: Visit URLs to download manually and place in server's plugins/mods folder\033[0m")
        input("\nPress Enter to continue...")
    
    def search_plugins(self):
        """Search for plugins"""
        os.system('clear')
        print("\033[1m\033[36m═══ SEARCH PLUGINS ═══\033[0m")
        print()
        
        query = input("Enter search query: ")
        
        print()
        print(f"\033[36m[INFO]\033[0m Searching for '{query}'...")
        print()
        
        # SpigotMC search
        print("\033[33mSpigotMC Results:\033[0m")
        print(f"  https://www.spigotmc.org/resources/?search={query}")
        print()
        
        # CurseForge search
        print("\033[33mCurseForge Results:\033[0m")
        print(f"  https://www.curseforge.com/minecraft/search?search={query}")
        print()
        
        # Modrinth search
        print("\033[33mModrinth Results:\033[0m")
        print(f"  https://modrinth.com/mods?q={query}")
        print()
        
        input("Press Enter to continue...")
    
    def install_from_url(self):
        """Install plugin from URL"""
        os.system('clear')
        print("\033[1m\033[36m═══ INSTALL FROM URL ═══\033[0m")
        print()
        
        # Select server
        servers = list(self.servers_dir.iterdir())
        if not servers:
            print("\033[31m[ERROR]\033[0m No servers found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server:")
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
        
        # Get URL
        print()
        url = input("Enter plugin/mod download URL: ")
        
        if not url:
            return
        
        # Determine if plugins or mods folder
        plugins_dir = server_path / "plugins"
        mods_dir = server_path / "mods"
        
        if plugins_dir.exists():
            target_dir = plugins_dir
        elif mods_dir.exists():
            target_dir = mods_dir
        else:
            # Create plugins folder by default
            plugins_dir.mkdir(parents=True, exist_ok=True)
            target_dir = plugins_dir
        
        # Download
        print()
        print(f"\033[36m[INFO]\033[0m Downloading...")
        
        try:
            response = requests.get(url, stream=True)
            filename = url.split("/")[-1]
            if not filename.endswith(".jar"):
                filename += ".jar"
            
            filepath = target_dir / filename
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
            
            print()
            print(f"\033[32m[SUCCESS]\033[0m Plugin installed to: {filepath}")
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def manage_server_plugins(self):
        """Manage plugins for a specific server"""
        os.system('clear')
        print("\033[1m\033[36m═══ MANAGE SERVER PLUGINS ═══\033[0m")
        print()
        
        # Select server
        servers = list(self.servers_dir.iterdir())
        if not servers:
            print("\033[31m[ERROR]\033[0m No servers found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server:")
        for i, server in enumerate(servers, 1):
            print(f"  \033[32m[{i}]\033[0m {server.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            server_path = servers[server_index]
        except:
            return
        
        # List plugins
        print()
        print(f"\033[36m[INFO]\033[0m Plugins/Mods for: {server_path.name}")
        print()
        
        plugins_dir = server_path / "plugins"
        mods_dir = server_path / "mods"
        
        plugins_found = False
        
        if plugins_dir.exists():
            plugins = list(plugins_dir.glob("*.jar"))
            if plugins:
                print("\033[33mPlugins:\033[0m")
                for plugin in plugins:
                    size = plugin.stat().st_size / 1024
                    print(f"  • {plugin.name} ({size:.1f} KB)")
                plugins_found = True
        
        if mods_dir.exists():
            mods = list(mods_dir.glob("*.jar"))
            if mods:
                print("\n\033[33mMods:\033[0m")
                for mod in mods:
                    size = mod.stat().st_size / 1024
                    print(f"  • {mod.name} ({size:.1f} KB)")
                plugins_found = True
        
        if not plugins_found:
            print("\033[90mNo plugins or mods installed\033[0m")
        
        input("\nPress Enter to continue...")
    
    def update_all_plugins(self):
        """Update all plugins"""
        print("\033[33m[INFO]\033[0m Plugin auto-update not implemented yet")
        print("\033[90mPlease check plugin sources manually for updates\033[0m")
        input("\nPress Enter to continue...")
    
    def remove_plugin(self):
        """Remove a plugin"""
        os.system('clear')
        print("\033[1m\033[36m═══ REMOVE PLUGIN ═══\033[0m")
        print()
        
        # Select server
        servers = list(self.servers_dir.iterdir())
        if not servers:
            print("\033[31m[ERROR]\033[0m No servers found")
            input("\nPress Enter to continue...")
            return
        
        print("Select server:")
        for i, server in enumerate(servers, 1):
            print(f"  \033[32m[{i}]\033[0m {server.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            server_index = int(choice) - 1
            server_path = servers[server_index]
        except:
            return
        
        # List plugins
        all_plugins = []
        plugins_dir = server_path / "plugins"
        mods_dir = server_path / "mods"
        
        if plugins_dir.exists():
            all_plugins.extend(list(plugins_dir.glob("*.jar")))
        if mods_dir.exists():
            all_plugins.extend(list(mods_dir.glob("*.jar")))
        
        if not all_plugins:
            print("\033[33m[WARN]\033[0m No plugins found")
            input("\nPress Enter to continue...")
            return
        
        print()
        print("Select plugin to remove:")
        for i, plugin in enumerate(all_plugins, 1):
            print(f"  \033[32m[{i}]\033[0m {plugin.name}")
        
        print()
        choice = input("Select: ")
        
        try:
            plugin_index = int(choice) - 1
            plugin_path = all_plugins[plugin_index]
            
            confirm = input(f"\033[33mRemove {plugin_path.name}? (y/n): \033[0m")
            if confirm.lower() == 'y':
                plugin_path.unlink()
                print(f"\033[32m[SUCCESS]\033[0m Plugin removed")
        except:
            print("\033[31m[ERROR]\033[0m Invalid selection")
        
        input("\nPress Enter to continue...")

def main():
    manager = PluginManager()
    manager.show_menu()

if __name__ == "__main__":
    main()

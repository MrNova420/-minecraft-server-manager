#!/usr/bin/env python3
"""
Minecraft Server Creator
Handles downloading and setting up different server types
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from tqdm import tqdm

class ServerCreator:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
        self.servers_dir.mkdir(parents=True, exist_ok=True)
        
        self.server_types = {
            "1": {"name": "Vanilla", "download_func": self.download_vanilla},
            "2": {"name": "Paper", "download_func": self.download_paper},
            "3": {"name": "Spigot", "download_func": self.download_spigot},
            "4": {"name": "Purpur", "download_func": self.download_purpur},
            "5": {"name": "Fabric", "download_func": self.download_fabric},
            "6": {"name": "Forge", "download_func": self.download_forge},
            "7": {"name": "NeoForge", "download_func": self.download_neoforge},
            "8": {"name": "BungeeCord", "download_func": self.download_bungeecord},
            "9": {"name": "Velocity", "download_func": self.download_velocity}
        }
    
    def create_server(self, name, server_type, version, ram, cores):
        """Create a new Minecraft server"""
        server_path = self.servers_dir / name
        server_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\033[36m[INFO]\033[0m Creating server '{name}'...")
        print(f"\033[36m[INFO]\033[0m Type: {self.server_types[server_type]['name']}")
        print(f"\033[36m[INFO]\033[0m Version: {version}")
        print(f"\033[36m[INFO]\033[0m RAM: {ram}MB")
        print(f"\033[36m[INFO]\033[0m CPU Cores: {cores}")
        
        # Download server jar
        print(f"\033[36m[INFO]\033[0m Downloading server files...")
        jar_path = self.server_types[server_type]['download_func'](server_path, version)
        
        if not jar_path:
            print(f"\033[31m[ERROR]\033[0m Failed to download server")
            return False
        
        # Create server configuration
        config = {
            "name": name,
            "type": self.server_types[server_type]['name'],
            "version": version,
            "ram": ram,
            "cores": cores,
            "jar_file": jar_path.name,
            "port": self.get_next_port(),
            "created": str(Path.cwd())
        }
        
        with open(server_path / "msm_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        # Create start script
        self.create_start_script(server_path, config)
        
        # Create default server.properties
        self.create_server_properties(server_path, config)
        
        # Accept EULA
        with open(server_path / "eula.txt", "w") as f:
            f.write("eula=true\n")
        
        # Create optimized JVM flags file
        self.create_jvm_flags(server_path, ram)
        
        print(f"\033[32m[SUCCESS]\033[0m Server created at: {server_path}")
        return True
    
    def download_vanilla(self, server_path, version):
        """Download Vanilla Minecraft server"""
        try:
            # Get version manifest
            manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
            response = requests.get(manifest_url)
            manifest = response.json()
            
            # Find version
            if version == "latest":
                version_data = manifest["latest"]["release"]
            else:
                version_data = version
            
            version_url = None
            for v in manifest["versions"]:
                if v["id"] == version_data:
                    version_url = v["url"]
                    break
            
            if not version_url:
                print(f"\033[31m[ERROR]\033[0m Version {version} not found")
                return None
            
            # Get server download URL
            version_response = requests.get(version_url)
            version_info = version_response.json()
            server_url = version_info["downloads"]["server"]["url"]
            
            # Download server jar
            jar_path = server_path / "server.jar"
            self.download_file(server_url, jar_path)
            
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_paper(self, server_path, version):
        """Download Paper server"""
        try:
            if version == "latest":
                version = "1.20.4"
            
            # Get latest build
            api_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print(f"\033[31m[ERROR]\033[0m Version {version} not found for Paper")
                return None
            
            builds = response.json()["builds"]
            latest_build = builds[-1]
            
            # Download Paper jar
            download_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/paper-{version}-{latest_build}.jar"
            jar_path = server_path / "server.jar"
            self.download_file(download_url, jar_path)
            
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_spigot(self, server_path, version):
        """Download Spigot server"""
        try:
            if version == "latest":
                version = "1.20.4"
            
            # Use GetBukkit mirror
            download_url = f"https://download.getbukkit.org/spigot/spigot-{version}.jar"
            jar_path = server_path / "server.jar"
            
            print(f"\033[33m[WARN]\033[0m Spigot may require manual download")
            print(f"\033[36m[INFO]\033[0m Attempting to download from mirror...")
            
            try:
                self.download_file(download_url, jar_path)
                return jar_path
            except:
                print(f"\033[33m[WARN]\033[0m Mirror failed, falling back to Paper")
                return self.download_paper(server_path, version)
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_purpur(self, server_path, version):
        """Download Purpur server"""
        try:
            if version == "latest":
                version = "1.20.4"
            
            # Get latest build
            api_url = f"https://api.purpurmc.org/v2/purpur/{version}"
            response = requests.get(api_url)
            if response.status_code != 200:
                print(f"\033[31m[ERROR]\033[0m Version {version} not found for Purpur")
                return None
            
            latest_build = response.json()["builds"]["latest"]
            
            # Download Purpur jar
            download_url = f"https://api.purpurmc.org/v2/purpur/{version}/{latest_build}/download"
            jar_path = server_path / "server.jar"
            self.download_file(download_url, jar_path)
            
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_fabric(self, server_path, version):
        """Download Fabric server"""
        try:
            if version == "latest":
                version = "1.20.4"
            
            # Download Fabric installer
            installer_url = "https://meta.fabricmc.net/v2/versions/loader"
            response = requests.get(installer_url)
            loaders = response.json()
            latest_loader = loaders[0]["version"]
            
            # Download Fabric server launcher
            download_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{latest_loader}/1.0.0/server/jar"
            jar_path = server_path / "server.jar"
            self.download_file(download_url, jar_path)
            
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_forge(self, server_path, version):
        """Download Forge server"""
        print(f"\033[33m[WARN]\033[0m Forge requires manual installation")
        print(f"\033[36m[INFO]\033[0m Please visit: https://files.minecraftforge.net/")
        print(f"\033[36m[INFO]\033[0m Download the installer and place it in: {server_path}")
        print(f"\033[36m[INFO]\033[0m Run: java -jar forge-installer.jar --installServer")
        
        # Create placeholder
        jar_path = server_path / "forge-installer.jar"
        return jar_path
    
    def download_neoforge(self, server_path, version):
        """Download NeoForge server"""
        print(f"\033[33m[WARN]\033[0m NeoForge requires manual installation")
        print(f"\033[36m[INFO]\033[0m Please visit: https://neoforged.net/")
        
        jar_path = server_path / "neoforge-installer.jar"
        return jar_path
    
    def download_bungeecord(self, server_path, version):
        """Download BungeeCord proxy"""
        try:
            download_url = "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"
            jar_path = server_path / "server.jar"
            self.download_file(download_url, jar_path)
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_velocity(self, server_path, version):
        """Download Velocity proxy"""
        try:
            if version == "latest":
                version = "3.3.0-SNAPSHOT"
            
            api_url = "https://api.papermc.io/v2/projects/velocity"
            response = requests.get(api_url)
            versions = response.json()["versions"]
            latest_version = versions[-1]
            
            # Get latest build
            builds_url = f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}"
            builds_response = requests.get(builds_url)
            latest_build = builds_response.json()["builds"][-1]
            
            download_url = f"https://api.papermc.io/v2/projects/velocity/versions/{latest_version}/builds/{latest_build}/downloads/velocity-{latest_version}-{latest_build}.jar"
            jar_path = server_path / "server.jar"
            self.download_file(download_url, jar_path)
            
            return jar_path
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {str(e)}")
            return None
    
    def download_file(self, url, destination):
        """Download file with progress bar"""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as f, tqdm(
            desc=destination.name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    def create_start_script(self, server_path, config):
        """Create optimized start script"""
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
        os.chmod(script_path, 0o755)
    
    def create_server_properties(self, server_path, config):
        """Create optimized server.properties"""
        properties = f"""server-port={config['port']}
max-players=100
view-distance=10
simulation-distance=8
online-mode=true
difficulty=normal
gamemode=survival
pvp=true
spawn-protection=16
enable-command-block=true
network-compression-threshold=256
max-tick-time=60000
use-native-transport=true
enable-status=true
enable-query=false
"""
        with open(server_path / "server.properties", "w") as f:
            f.write(properties)
    
    def create_jvm_flags(self, server_path, ram):
        """Create optimized JVM flags for Termux/Android"""
        # Simplified flags that work on Android
        flags = """-XX:+UseG1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
-XX:+UnlockExperimentalVMOptions
-XX:G1NewSizePercent=30
-XX:G1MaxNewSizePercent=40
-XX:G1HeapRegionSize=8M
-XX:G1ReservePercent=20
-XX:InitiatingHeapOccupancyPercent=15
-XX:MaxTenuringThreshold=1
"""
        with open(server_path / "jvm_flags.txt", "w") as f:
            f.write(flags)
    
    def get_next_port(self):
        """Get next available server port"""
        ports = []
        for server_dir in self.servers_dir.iterdir():
            if server_dir.is_dir():
                config_file = server_dir / "msm_config.json"
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                        ports.append(config.get("port", 25565))
        
        base_port = 25565
        while base_port in ports:
            base_port += 1
        return base_port

def main():
    parser = argparse.ArgumentParser(description='Minecraft Server Creator')
    parser.add_argument('--name', required=True, help='Server name')
    parser.add_argument('--type', required=True, help='Server type (1-9)')
    parser.add_argument('--version', default='latest', help='Minecraft version')
    parser.add_argument('--ram', type=int, default=2048, help='RAM in MB')
    parser.add_argument('--cores', type=int, default=2, help='CPU cores')
    
    args = parser.parse_args()
    
    creator = ServerCreator()
    creator.create_server(args.name, args.type, args.version, args.ram, args.cores)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Minecraft Server Manager
Handles starting, stopping, and managing servers
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
        self.servers_dir.mkdir(parents=True, exist_ok=True)
    
    def start_server(self, server_name):
        """Start a Minecraft server"""
        server_path = self.servers_dir / server_name
        
        if not server_path.exists():
            print(f"\033[31m[ERROR]\033[0m Server '{server_name}' not found")
            return False
        
        config_file = server_path / "msm_config.json"
        if not config_file.exists():
            print(f"\033[31m[ERROR]\033[0m Server configuration not found")
            return False
        
        with open(config_file) as f:
            config = json.load(f)
        
        # Check if already running
        result = subprocess.run(
            ["screen", "-list"],
            capture_output=True,
            text=True
        )
        
        if f"msm-{server_name}" in result.stdout:
            print(f"\033[33m[WARN]\033[0m Server is already running")
            return False
        
        # Start server in screen session
        print(f"\033[36m[INFO]\033[0m Starting server '{server_name}'...")
        print(f"\033[36m[INFO]\033[0m RAM: {config['ram']}MB")
        print(f"\033[36m[INFO]\033[0m Cores: {config['cores']}")
        print(f"\033[36m[INFO]\033[0m Port: {config['port']}")
        
        start_script = server_path / "start.sh"
        
        subprocess.run([
            "screen", "-dmS", f"msm-{server_name}",
            "bash", str(start_script)
        ])
        
        time.sleep(2)
        
        # Verify server started
        result = subprocess.run(
            ["screen", "-list"],
            capture_output=True,
            text=True
        )
        
        if f"msm-{server_name}" in result.stdout:
            print(f"\033[32m[SUCCESS]\033[0m Server started successfully!")
            print(f"\033[36m[INFO]\033[0m Screen session: msm-{server_name}")
            print(f"\033[36m[INFO]\033[0m To attach: screen -r msm-{server_name}")
            return True
        else:
            print(f"\033[31m[ERROR]\033[0m Failed to start server")
            return False
    
    def stop_server(self, server_name):
        """Stop a Minecraft server"""
        # Check if running
        result = subprocess.run(
            ["screen", "-list"],
            capture_output=True,
            text=True
        )
        
        if f"msm-{server_name}" not in result.stdout:
            print(f"\033[33m[WARN]\033[0m Server is not running")
            return False
        
        print(f"\033[36m[INFO]\033[0m Stopping server '{server_name}'...")
        
        # Send stop command to server
        subprocess.run([
            "screen", "-S", f"msm-{server_name}",
            "-X", "stuff", "stop\n"
        ])
        
        # Wait for server to stop
        print(f"\033[36m[INFO]\033[0m Waiting for server to shut down...")
        for i in range(30):
            time.sleep(1)
            result = subprocess.run(
                ["screen", "-list"],
                capture_output=True,
                text=True
            )
            if f"msm-{server_name}" not in result.stdout:
                print(f"\033[32m[SUCCESS]\033[0m Server stopped successfully!")
                return True
        
        # Force kill if not stopped
        print(f"\033[33m[WARN]\033[0m Server did not stop gracefully, forcing...")
        subprocess.run([
            "screen", "-S", f"msm-{server_name}", "-X", "quit"
        ])
        
        print(f"\033[32m[SUCCESS]\033[0m Server stopped!")
        return True
    
    def restart_server(self, server_name):
        """Restart a Minecraft server"""
        print(f"\033[36m[INFO]\033[0m Restarting server '{server_name}'...")
        self.stop_server(server_name)
        time.sleep(3)
        self.start_server(server_name)
    
    def list_servers(self):
        """List all servers and their status"""
        if not self.servers_dir.exists() or not any(self.servers_dir.iterdir()):
            print(f"\033[33m[WARN]\033[0m No servers found")
            return
        
        # Get running servers
        result = subprocess.run(
            ["screen", "-list"],
            capture_output=True,
            text=True
        )
        running_servers = result.stdout
        
        print("\n\033[1m\033[36m═══════════ SERVER LIST ═══════════\033[0m\n")
        
        for server_dir in sorted(self.servers_dir.iterdir()):
            if server_dir.is_dir():
                server_name = server_dir.name
                config_file = server_dir / "msm_config.json"
                
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                    
                    status = "\033[32m[RUNNING]\033[0m" if f"msm-{server_name}" in running_servers else "\033[31m[STOPPED]\033[0m"
                    
                    print(f"  \033[1m{server_name}\033[0m {status}")
                    print(f"    Type: {config['type']}")
                    print(f"    Version: {config['version']}")
                    print(f"    RAM: {config['ram']}MB")
                    print(f"    Port: {config['port']}")
                    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: server_manager.py <start|stop|restart|list|manage> [server_name]")
        sys.exit(1)
    
    manager = ServerManager()
    command = sys.argv[1]
    
    if command == "list" or command == "manage":
        manager.list_servers()
    elif command in ["start", "stop", "restart"]:
        if len(sys.argv) < 3:
            print(f"\033[31m[ERROR]\033[0m Server name required")
            sys.exit(1)
        
        server_name = sys.argv[2]
        
        if command == "start":
            manager.start_server(server_name)
        elif command == "stop":
            manager.stop_server(server_name)
        elif command == "restart":
            manager.restart_server(server_name)
    else:
        print(f"\033[31m[ERROR]\033[0m Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

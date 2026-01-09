#!/usr/bin/env python3
"""
Server Status Display
Show detailed server status and information
"""

import os
import sys
import json
import subprocess
import psutil
from pathlib import Path
from datetime import datetime

class ServerStatus:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
    
    def display_status(self):
        """Display comprehensive server status"""
        os.system('clear')
        
        print("\033[1m\033[36m╔══════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[1m\033[36m║                   SERVER STATUS                              ║\033[0m")
        print("\033[1m\033[36m╚══════════════════════════════════════════════════════════════╝\033[0m")
        print()
        
        # System info
        print("\033[1m\033[33m═══ SYSTEM INFORMATION ═══\033[0m")
        print()
        
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(Path.home()))
        
        print(f"  \033[1mCPU:\033[0m {cpu_count} cores @ {cpu_percent:.1f}% usage")
        print(f"  \033[1mRAM:\033[0m {memory.used/1024/1024:.0f}MB / {memory.total/1024/1024:.0f}MB ({memory.percent:.1f}%)")
        print(f"  \033[1mDisk:\033[0m {disk.used/1024/1024/1024:.1f}GB / {disk.total/1024/1024/1024:.1f}GB ({disk.percent:.1f}%)")
        print()
        
        # Get running screen sessions
        result = subprocess.run(
            ["screen", "-list"],
            capture_output=True,
            text=True
        )
        running_sessions = result.stdout
        
        # Server information
        if not self.servers_dir.exists() or not any(self.servers_dir.iterdir()):
            print("\033[1m\033[33m═══ SERVERS ═══\033[0m")
            print()
            print("\033[90m  No servers found\033[0m")
            print()
        else:
            servers = []
            running_count = 0
            
            for server_dir in sorted(self.servers_dir.iterdir()):
                if server_dir.is_dir():
                    config_file = server_dir / "msm_config.json"
                    if config_file.exists():
                        with open(config_file) as f:
                            config = json.load(f)
                        
                        is_running = f"msm-{server_dir.name}" in running_sessions
                        if is_running:
                            running_count += 1
                        
                        servers.append({
                            'name': server_dir.name,
                            'config': config,
                            'running': is_running,
                            'path': server_dir
                        })
            
            print("\033[1m\033[33m═══ SERVERS ═══\033[0m")
            print()
            print(f"  Total: {len(servers)} | Running: \033[32m{running_count}\033[0m | Stopped: \033[31m{len(servers) - running_count}\033[0m")
            print()
            
            for server in servers:
                status = "\033[32m● RUNNING\033[0m" if server['running'] else "\033[31m● STOPPED\033[0m"
                print(f"  {status} \033[1m{server['name']}\033[0m")
                print(f"    Type: {server['config']['type']} | Version: {server['config']['version']}")
                print(f"    RAM: {server['config']['ram']}MB | Cores: {server['config']['cores']} | Port: {server['config']['port']}")
                
                if server['running']:
                    # Try to get process info
                    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                        try:
                            if 'java' in proc.info['name'].lower():
                                cmdline = ' '.join(proc.cmdline())
                                if server['name'] in cmdline or str(server['path']) in cmdline:
                                    cpu = proc.cpu_percent(interval=0.1)
                                    mem = proc.info['memory_info'].rss / 1024 / 1024
                                    print(f"    \033[90mCPU: {cpu:.1f}% | RAM: {mem:.0f}MB | PID: {proc.info['pid']}\033[0m")
                                    break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                
                # Check world size
                world_dir = server['path'] / "world"
                if world_dir.exists():
                    size = sum(f.stat().st_size for f in world_dir.rglob('*') if f.is_file())
                    size_mb = size / 1024 / 1024
                    print(f"    \033[90mWorld size: {size_mb:.1f}MB\033[0m")
                
                print()
        
        # Network information
        print("\033[1m\033[33m═══ NETWORK ═══\033[0m")
        print()
        
        # Get local IP
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"  \033[1mLocal IP:\033[0m {local_ip}")
        except:
            print(f"  \033[1mLocal IP:\033[0m Unable to detect")
        
        # Check internet connection
        try:
            response = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"],
                capture_output=True,
                timeout=2
            )
            if response.returncode == 0:
                print(f"  \033[1mInternet:\033[0m \033[32m● Connected\033[0m")
            else:
                print(f"  \033[1mInternet:\033[0m \033[31m● Disconnected\033[0m")
        except:
            print(f"  \033[1mInternet:\033[0m \033[33m● Unknown\033[0m")
        
        print()
        
        # Recent activity
        print("\033[1m\033[33m═══ QUICK ACTIONS ═══\033[0m")
        print()
        print("  Run \033[1m./msm.sh\033[0m to access the main menu")
        print()
        
        input("\033[90mPress Enter to return...\033[0m")

def main():
    status = ServerStatus()
    status.display_status()

if __name__ == "__main__":
    main()

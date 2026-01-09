#!/usr/bin/env python3
"""
Resource Monitor
Real-time monitoring of server resources
"""

import os
import sys
import time
import psutil
import subprocess
from pathlib import Path
import json

class ResourceMonitor:
    def __init__(self):
        self.data_dir = Path.home() / ".msm"
        self.servers_dir = self.data_dir / "servers"
    
    def get_server_processes(self):
        """Get all running Minecraft server processes"""
        servers = {}
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'java' in proc.info['name'].lower():
                    # Check if it's a Minecraft server
                    cmdline_str = ' '.join(cmdline)
                    if 'server.jar' in cmdline_str or 'minecraft' in cmdline_str.lower():
                        # Extract server name from screen session
                        result = subprocess.run(
                            ["screen", "-list"],
                            capture_output=True,
                            text=True
                        )
                        
                        for line in result.stdout.split('\n'):
                            if 'msm-' in line and str(proc.info['pid']) in line:
                                server_name = line.split('msm-')[1].split('\t')[0].strip()
                                servers[server_name] = {
                                    'pid': proc.info['pid'],
                                    'cpu': proc.cpu_percent(interval=0.1),
                                    'memory': proc.info['memory_info'].rss / 1024 / 1024,  # MB
                                    'process': proc
                                }
                                break
            except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
                pass
        
        return servers
    
    def get_system_stats(self):
        """Get overall system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5, percpu=False)
            cpu_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        except (PermissionError, Exception):
            # Fallback for Android/Termux
            cpu_percent = 0
            cpu_per_core = [0, 0]
        
        try:
            memory = psutil.virtual_memory()
        except (PermissionError, Exception):
            # Fallback values
            class FakeMemory:
                total = 4096 * 1024 * 1024
                available = 2048 * 1024 * 1024
                used = 2048 * 1024 * 1024
                percent = 50
            memory = FakeMemory()
        
        try:
            disk = psutil.disk_usage(str(Path.home()))
        except (PermissionError, Exception):
            class FakeDisk:
                total = 64 * 1024 * 1024 * 1024
                used = 32 * 1024 * 1024 * 1024
                free = 32 * 1024 * 1024 * 1024
                percent = 50
            disk = FakeDisk()
        
        return {
            'cpu': {
                'overall': cpu_percent,
                'per_core': cpu_per_core,
                'cores': len(cpu_per_core)
            },
            'memory': {
                'total': memory.total / 1024 / 1024,  # MB
                'available': memory.available / 1024 / 1024,
                'used': memory.used / 1024 / 1024,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total / 1024 / 1024 / 1024,  # GB
                'used': disk.used / 1024 / 1024 / 1024,
                'free': disk.free / 1024 / 1024 / 1024,
                'percent': disk.percent
            }
        }
    
    def display_monitor(self):
        """Display real-time resource monitor"""
        try:
            while True:
                os.system('clear')
                
                print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
                print("\033[1m\033[36m║            RESOURCE MONITOR - LIVE VIEW                  ║\033[0m")
                print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
                print()
                
                # System stats
                stats = self.get_system_stats()
                
                print("\033[1m\033[33m═══ SYSTEM RESOURCES ═══\033[0m")
                print()
                
                # CPU
                print(f"  \033[1mCPU Usage:\033[0m {stats['cpu']['overall']:.1f}%")
                print("  " + self.create_bar(stats['cpu']['overall'], 100, 40))
                print(f"  \033[90mCores: {stats['cpu']['cores']}\033[0m")
                for i, core_percent in enumerate(stats['cpu']['per_core']):
                    bar = self.create_bar(core_percent, 100, 20, compact=True)
                    print(f"    Core {i}: {bar} {core_percent:.1f}%")
                print()
                
                # Memory
                print(f"  \033[1mMemory:\033[0m {stats['memory']['used']:.0f}MB / {stats['memory']['total']:.0f}MB ({stats['memory']['percent']:.1f}%)")
                print("  " + self.create_bar(stats['memory']['percent'], 100, 40))
                print(f"  \033[90mAvailable: {stats['memory']['available']:.0f}MB\033[0m")
                print()
                
                # Disk
                print(f"  \033[1mDisk:\033[0m {stats['disk']['used']:.1f}GB / {stats['disk']['total']:.1f}GB ({stats['disk']['percent']:.1f}%)")
                print("  " + self.create_bar(stats['disk']['percent'], 100, 40))
                print(f"  \033[90mFree: {stats['disk']['free']:.1f}GB\033[0m")
                print()
                
                # Server processes
                servers = self.get_server_processes()
                
                if servers:
                    print("\033[1m\033[33m═══ MINECRAFT SERVERS ═══\033[0m")
                    print()
                    
                    for server_name, info in servers.items():
                        print(f"  \033[1m\033[32m● {server_name}\033[0m")
                        print(f"    PID: {info['pid']}")
                        print(f"    CPU: {info['cpu']:.1f}%")
                        print(f"    RAM: {info['memory']:.0f}MB")
                        
                        # Get network connections
                        try:
                            connections = info['process'].connections()
                            for conn in connections:
                                if conn.status == 'LISTEN':
                                    print(f"    Port: {conn.laddr.port}")
                                    break
                        except:
                            pass
                        print()
                else:
                    print("\033[1m\033[33m═══ MINECRAFT SERVERS ═══\033[0m")
                    print()
                    print("  \033[90mNo servers running\033[0m")
                    print()
                
                # Network stats
                net_io = psutil.net_io_counters()
                print("\033[1m\033[33m═══ NETWORK ═══\033[0m")
                print(f"  Sent: {net_io.bytes_sent / 1024 / 1024:.1f}MB")
                print(f"  Received: {net_io.bytes_recv / 1024 / 1024:.1f}MB")
                print()
                
                print("\033[90mPress Ctrl+C to exit | Updating every 2 seconds\033[0m")
                
                time.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\033[32m[INFO]\033[0m Exiting monitor...")
            sys.exit(0)
    
    def create_bar(self, value, max_value, width, compact=False):
        """Create a visual progress bar"""
        percent = min(value / max_value, 1.0)
        filled = int(width * percent)
        empty = width - filled
        
        # Color based on percentage
        if percent < 0.5:
            color = '\033[32m'  # Green
        elif percent < 0.8:
            color = '\033[33m'  # Yellow
        else:
            color = '\033[31m'  # Red
        
        if compact:
            bar = color + '█' * filled + '\033[90m░\033[0m' * empty + '\033[0m'
        else:
            bar = '[' + color + '█' * filled + '\033[90m' + '░' * empty + '\033[0m]'
        
        return bar

def main():
    monitor = ResourceMonitor()
    monitor.display_monitor()

if __name__ == "__main__":
    main()

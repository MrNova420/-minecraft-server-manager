#!/usr/bin/env python3
"""
Web Control Panel
Web-based interface for server management
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_DIR = Path.home() / ".msm"
SERVERS_DIR = DATA_DIR / "servers"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Minecraft Server Manager</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            padding: 30px 0;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
        }
        .servers {
            display: grid;
            gap: 20px;
        }
        .server-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .server-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .server-name {
            font-size: 1.5em;
            font-weight: bold;
        }
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .status-running {
            background: #10b981;
        }
        .status-stopped {
            background: #ef4444;
        }
        .server-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        .info-item {
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 8px;
        }
        .info-label {
            font-size: 0.8em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 1.1em;
            font-weight: bold;
        }
        .actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn-start {
            background: #10b981;
            color: white;
        }
        .btn-stop {
            background: #ef4444;
            color: white;
        }
        .btn-restart {
            background: #f59e0b;
            color: white;
        }
        .btn-console {
            background: #3b82f6;
            color: white;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 1.8em; }
            .stats { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 Minecraft Server Manager</h1>
            <p>Professional Android Server Hosting</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3>CPU Usage</h3>
                <div class="value" id="cpu">--%</div>
            </div>
            <div class="stat-card">
                <h3>Memory</h3>
                <div class="value" id="memory">-- MB</div>
            </div>
            <div class="stat-card">
                <h3>Active Servers</h3>
                <div class="value" id="active-servers">0</div>
            </div>
            <div class="stat-card">
                <h3>Total Servers</h3>
                <div class="value" id="total-servers">0</div>
            </div>
        </div>
        
        <div class="servers" id="servers">
            <!-- Servers will be loaded here -->
        </div>
    </div>
    
    <script>
        function loadServers() {
            fetch('/api/servers')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('servers');
                    container.innerHTML = '';
                    
                    data.servers.forEach(server => {
                        const card = document.createElement('div');
                        card.className = 'server-card';
                        
                        const statusClass = server.running ? 'status-running' : 'status-stopped';
                        const statusText = server.running ? 'RUNNING' : 'STOPPED';
                        
                        card.innerHTML = `
                            <div class="server-header">
                                <div class="server-name">${server.name}</div>
                                <div class="status-badge ${statusClass}">${statusText}</div>
                            </div>
                            <div class="server-info">
                                <div class="info-item">
                                    <div class="info-label">Type</div>
                                    <div class="info-value">${server.type}</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">Version</div>
                                    <div class="info-value">${server.version}</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">RAM</div>
                                    <div class="info-value">${server.ram} MB</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">Port</div>
                                    <div class="info-value">${server.port}</div>
                                </div>
                            </div>
                            <div class="actions">
                                <button class="btn btn-start" onclick="startServer('${server.name}')" ${server.running ? 'disabled' : ''}>
                                    Start
                                </button>
                                <button class="btn btn-stop" onclick="stopServer('${server.name}')" ${!server.running ? 'disabled' : ''}>
                                    Stop
                                </button>
                                <button class="btn btn-restart" onclick="restartServer('${server.name}')" ${!server.running ? 'disabled' : ''}>
                                    Restart
                                </button>
                                <button class="btn btn-console" ${!server.running ? 'disabled' : ''}>
                                    Console
                                </button>
                            </div>
                        `;
                        
                        container.appendChild(card);
                    });
                    
                    document.getElementById('total-servers').textContent = data.servers.length;
                    document.getElementById('active-servers').textContent = 
                        data.servers.filter(s => s.running).length;
                });
        }
        
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('cpu').textContent = data.cpu.toFixed(1) + '%';
                    document.getElementById('memory').textContent = 
                        data.memory.used.toFixed(0) + ' / ' + data.memory.total.toFixed(0) + ' MB';
                });
        }
        
        function startServer(name) {
            fetch('/api/server/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            }).then(() => setTimeout(loadServers, 2000));
        }
        
        function stopServer(name) {
            fetch('/api/server/stop', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            }).then(() => setTimeout(loadServers, 2000));
        }
        
        function restartServer(name) {
            stopServer(name);
            setTimeout(() => startServer(name), 5000);
        }
        
        // Load data
        loadServers();
        loadStats();
        
        // Refresh every 5 seconds
        setInterval(loadServers, 5000);
        setInterval(loadStats, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/servers')
def api_servers():
    servers = []
    
    if SERVERS_DIR.exists():
        for server_dir in SERVERS_DIR.iterdir():
            if server_dir.is_dir():
                config_file = server_dir / "msm_config.json"
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                    
                    # Check if running
                    result = subprocess.run(
                        ["screen", "-list"],
                        capture_output=True,
                        text=True
                    )
                    running = f"msm-{server_dir.name}" in result.stdout
                    
                    servers.append({
                        "name": server_dir.name,
                        "type": config.get("type", "Unknown"),
                        "version": config.get("version", "Unknown"),
                        "ram": config.get("ram", 0),
                        "port": config.get("port", 0),
                        "cores": config.get("cores", 0),
                        "running": running
                    })
    
    return jsonify({"servers": servers})

@app.route('/api/stats')
def api_stats():
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        return jsonify({
            "cpu": cpu,
            "memory": {
                "total": memory.total / 1024 / 1024,
                "used": memory.used / 1024 / 1024,
                "percent": memory.percent
            }
        })
    except (PermissionError, Exception) as e:
        # Fallback for Android/Termux where /proc/stat is restricted
        return jsonify({
            "cpu": 0,
            "memory": {
                "total": 4096,
                "used": 2048,
                "percent": 50
            }
        })

@app.route('/api/server/start', methods=['POST'])
def api_server_start():
    data = request.json
    server_name = data.get('name')
    
    subprocess.Popen([
        sys.executable,
        str(Path(__file__).parent / "server_manager.py"),
        "start",
        server_name
    ])
    
    return jsonify({"status": "starting"})

@app.route('/api/server/stop', methods=['POST'])
def api_server_stop():
    data = request.json
    server_name = data.get('name')
    
    subprocess.Popen([
        sys.executable,
        str(Path(__file__).parent / "server_manager.py"),
        "stop",
        server_name
    ])
    
    return jsonify({"status": "stopping"})

def main():
    print("\033[1m\033[36m╔══════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1m\033[36m║              WEB CONTROL PANEL                           ║\033[0m")
    print("\033[1m\033[36m╚══════════════════════════════════════════════════════════╝\033[0m")
    print()
    print("\033[32m[INFO]\033[0m Starting web server...")
    print()
    print("\033[33mAccess the control panel at:\033[0m")
    print()
    print("  \033[1mhttp://localhost:8080\033[0m")
    print()
    print("\033[90mPress Ctrl+C to stop\033[0m")
    print()
    
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == "__main__":
    main()

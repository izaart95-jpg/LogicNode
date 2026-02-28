#!/usr/bin/env python3
"""
ESPectre Motion Detection WebSocket Server
Streams ESPHome CSI motion detection data to web dashboard
"""

import asyncio
import json
import re
import subprocess
import sys
from datetime import datetime
from typing import Set, Optional, Any
import websockets

# Handle different websockets versions
try:
    from websockets.asyncio.server import ServerConnection
    WebSocketConnection = ServerConnection
except ImportError:
    try:
        from websockets.server import WebSocketServerProtocol
        WebSocketConnection = WebSocketServerProtocol
    except ImportError:
        WebSocketConnection = Any  # Fallback

# Configuration
WEBSOCKET_PORT = 8765
HTTP_PORT = 8080

# Store connected clients
clients: Set[WebSocketConnection] = set()

# Store recent history (last 100 readings)
history = []
MAX_HISTORY = 100


class ESPHomeLogParser:
    """Parse ESPHome log output for motion detection metrics"""
    
    # Regex patterns for log parsing
    MOTION_PATTERN = re.compile(
        r'\[([^\]]+)\]\[I\]\[espectre:\d+\]\[wifi\]: '
        r'\[([^\]]+)\] (\d+)% \| '
        r'mvmt:([\d.]+) thr:([\d.]+) \| '
        r'(\w+) \| '
        r'(\d+) pkt/s \| '
        r'ch:(\d+) rssi:(-?\d+)'
    )
    
    MOVEMENT_SCORE_PATTERN = re.compile(
        r'\[D\]\[sensor:\d+\]\[wifi\]: \'Movement Score\' >> ([\d.]+)'
    )
    
    MOTION_STATE_PATTERN = re.compile(
        r'\[D\]\[binary_sensor:\d+\]\[wifi\]: \'Motion Detected\' >> (ON|OFF)'
    )
    
    CONFIG_THRESHOLD_PATTERN = re.compile(
        r'├─ Threshold \.+ ([\d.]+)'
    )
    
    CONFIG_DETECTOR_PATTERN = re.compile(
        r'├─ Detector \.+ (\w+)'
    )
    
    def __init__(self):
        self.current_threshold = 3.13  # Default
        self.detector_type = "MVS"  # Default
        
    def parse_config_line(self, line: str) -> Optional[dict]:
        """Parse configuration lines during startup"""
        threshold_match = self.CONFIG_THRESHOLD_PATTERN.search(line)
        if threshold_match:
            self.current_threshold = float(threshold_match.group(1))
            return {
                'type': 'config',
                'key': 'threshold',
                'value': self.current_threshold
            }
        
        detector_match = self.CONFIG_DETECTOR_PATTERN.search(line)
        if detector_match:
            self.detector_type = detector_match.group(1)
            return {
                'type': 'config',
                'key': 'detector',
                'value': self.detector_type
            }
        
        return None
    
    def parse_motion_line(self, line: str) -> Optional[dict]:
        """Parse motion detection log line"""
        match = self.MOTION_PATTERN.search(line)
        if not match:
            return None
        
        timestamp_str, bar_viz, percentage, movement, threshold, state, pkt_rate, channel, rssi = match.groups()
        
        data = {
            'type': 'motion_data',
            'timestamp': datetime.now().isoformat(),
            'movement_score': float(movement),
            'threshold': float(threshold),
            'state': state,
            'percentage': int(percentage),
            'packet_rate': int(pkt_rate),
            'channel': int(channel),
            'rssi': int(rssi),
            'bar_visualization': bar_viz,
            'detector': self.detector_type
        }
        
        return data
    
    def parse_line(self, line: str) -> Optional[dict]:
        """Parse any log line and return structured data"""
        # Try config parsing first
        config_data = self.parse_config_line(line)
        if config_data:
            return config_data
        
        # Try motion data parsing
        motion_data = self.parse_motion_line(line)
        if motion_data:
            return motion_data
        
        return None


async def register_client(websocket: WebSocketConnection):
    """Register a new WebSocket client"""
    clients.add(websocket)
    print(f"Client connected. Total clients: {len(clients)}")
    
    # Send connection confirmation
    await websocket.send(json.dumps({
        'type': 'connection',
        'status': 'connected',
        'timestamp': datetime.now().isoformat()
    }))
    
    # Send recent history to new client
    if history:
        await websocket.send(json.dumps({
            'type': 'history',
            'data': history[-50:]  # Send last 50 readings
        }))


async def unregister_client(websocket: WebSocketConnection):
    """Unregister a WebSocket client"""
    clients.discard(websocket)
    print(f"Client disconnected. Total clients: {len(clients)}")


async def broadcast_data(data: dict):
    """Broadcast data to all connected clients"""
    if not clients:
        return
    
    message = json.dumps(data)
    
    # Send to all clients, remove any that fail
    disconnected = set()
    for client in clients:
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            disconnected.add(client)
    
    # Clean up disconnected clients
    for client in disconnected:
        clients.discard(client)


async def stream_esphome_logs(device: str, use_ota: bool = True, verbose: bool = False):
    """Stream ESPHome logs and broadcast parsed data"""
    parser = ESPHomeLogParser()
    
    # Build command
    if use_ota:
        cmd = ['esphome', 'logs', 'espectre.yaml', '--device', 'OTA']
    else:
        cmd = ['esphome', 'logs', 'espectre.yaml', '--device', device]
    
    print(f"Starting ESPHome log stream: {' '.join(cmd)}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        print("ESPHome process started, waiting for data...")
        
        async for line in process.stdout:
            try:
                line_str = line.decode('utf-8', errors='ignore').strip()
                
                if not line_str:
                    continue
                
                # Print raw line if verbose mode enabled
                if verbose:
                    print(f"[RAW] {line_str}")
                
                # Parse the line
                data = parser.parse_line(line_str)
                
                if data:
                    # Add to history if it's motion data
                    if data['type'] == 'motion_data':
                        history.append(data)
                        if len(history) > MAX_HISTORY:
                            history.pop(0)
                    
                    # Broadcast to all clients
                    await broadcast_data(data)
                    
                    # Print summary
                    if data['type'] == 'motion_data':
                        bar = data.get('bar_visualization', '???')
                        pct = data.get('percentage', 0)
                        mvmt = data['movement_score']
                        thr = data['threshold']
                        state = data['state']
                        pkt = data['packet_rate']
                        ch = data['channel']
                        rssi = data['rssi']
                        
                        print(f"📊 [{bar}] {pct}% | mvmt:{mvmt:.4f} thr:{thr:.4f} | "
                              f"{state} | {pkt} pkt/s | ch:{ch} rssi:{rssi} | "
                              f"Clients: {len(clients)}")
                
            except Exception as e:
                print(f"Error parsing line: {e}")
                continue
        
        await process.wait()
        print("ESPHome process ended")
        
    except Exception as e:
        print(f"Error streaming logs: {e}")
        await broadcast_data({
            'type': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })


async def websocket_handler(websocket: WebSocketConnection):
    """Handle WebSocket connections"""
    await register_client(websocket)
    
    try:
        # Keep connection alive and handle incoming messages
        async for message in websocket:
            # Echo or handle client messages if needed
            try:
                data = json.loads(message)
                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({
                        'type': 'pong',
                        'timestamp': datetime.now().isoformat()
                    }))
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister_client(websocket)


async def start_websocket_server():
    """Start the WebSocket server"""
    print(f"Starting WebSocket server on port {WEBSOCKET_PORT}...")
    async with websockets.serve(websocket_handler, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()  # Run forever


async def serve_http():
    """Simple HTTP server for the dashboard"""
    try:
        from aiohttp import web
    except ImportError:
        print("aiohttp not installed. Install with: pip install aiohttp")
        print("Skipping HTTP server. Open dashboard.html directly in browser.")
        return
    
    async def handle_index(request):
        try:
            with open('dashboard.html', 'r') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        except FileNotFoundError:
            return web.Response(text="Dashboard not found", status=404)
    
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
    await site.start()
    
    print(f"HTTP server started on http://0.0.0.0:{HTTP_PORT}")


async def main(device: str = "OTA", use_ota: bool = True, verbose: bool = False):
    """Main entry point"""
    print("=" * 60)
    print("ESPectre Motion Detection WebSocket Server")
    print("=" * 60)
    if verbose:
        print("🔊 VERBOSE MODE ENABLED - Showing all ESPHome logs")
    
    # Start HTTP server (optional)
    try:
        await serve_http()
    except:
        pass
    
    # Start WebSocket server and ESPHome log streamer concurrently
    await asyncio.gather(
        start_websocket_server(),
        stream_esphome_logs(device, use_ota, verbose)
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ESPectre Motion Detection WebSocket Server')
    parser.add_argument('--device', default='OTA', 
                       help='Device address (use "OTA" for automatic discovery or IP like "10.117.195.48")')
    parser.add_argument('--port', type=int, default=8765,
                       help='WebSocket port (default: 8765)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose mode (show all raw ESPHome logs)')
    
    args = parser.parse_args()
    
    WEBSOCKET_PORT = args.port
    use_ota = args.device == "OTA"
    
    print(f"Device: {args.device}")
    print(f"WebSocket Port: {WEBSOCKET_PORT}")
    print(f"Dashboard: http://localhost:{HTTP_PORT}")
    print()
    
    try:
        asyncio.run(main(args.device, use_ota, args.verbose))
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
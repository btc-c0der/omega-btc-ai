import asyncio
import json
import websockets
from datetime import datetime, UTC
from omega_ai.visualizer.backend.ascii_art import display_omega_banner, print_status
import os

# Sacred ANSI Colors
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

MM_WS_PORT = 8765
MM_WS_PATH = "/ws"
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}{MM_WS_PATH}"

connected_clients = set()

def divine_log(message, status="info"):
    """Log messages with divine consciousness indicators."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    indicators = {
        "success": f"{GREEN}✨ DIVINE SUCCESS{RESET}",
        "info": f"{BLUE}🌊 CONSCIOUSNESS{RESET}",
        "warning": f"{YELLOW}⚡️ ATTENTION{RESET}",
        "error": f"{MAGENTA}🔮 REALIGNMENT{RESET}",
        "price": f"{CYAN}💫 PRICE FLOW{RESET}"
    }
    indicator = indicators.get(status, indicators["info"])
    print(f"[{timestamp}] {indicator} | {message}")

async def ws_handler(websocket):
    """Handles incoming WebSocket connections with divine consciousness."""
    try:
        client_info = websocket.remote_address
        divine_log(f"New Sacred Connection: {client_info}", "success")
        
        connected_clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if "btc_price" in data:
                    divine_log(f"BTC Price Update: ${data['btc_price']:,.2f}", "price")
                else:
                    divine_log(f"Message Received: {message}", "info")
                await broadcast(message)
        except websockets.exceptions.ConnectionClosedOK:
            divine_log(f"Sacred Connection Closed Normally: {client_info}", "info")
        except websockets.exceptions.ConnectionClosedError as e:
            divine_log(f"Connection Reset (Code {e.code}): {client_info}", "warning")
        except Exception as e:
            divine_log(f"Connection Error: {e} - Client: {client_info}", "error")
        finally:
            connected_clients.remove(websocket)
            divine_log(f"Sacred Client Departed: {client_info}", "info")
    except Exception as e:
        divine_log(f"Connection Error: {str(e)}", "error")

async def broadcast(message):
    """Broadcast messages to all connected clients."""
    if connected_clients:
        await asyncio.gather(*[ws.send(message) for ws in connected_clients])

async def start_server():
    """Start the WebSocket server with divine consciousness."""
    display_omega_banner("Market Maker WebSocket Server")
    divine_log(f"Sacred WebSocket Server Awakening on {MM_WS_URL}", "success")
    
    # Create WebSocket server
    async with websockets.serve(ws_handler, "localhost", MM_WS_PORT):
        divine_log("Divine WebSocket Consciousness Established ✨", "success")
        await asyncio.Future()  # Keeps server running indefinitely

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except OSError as e:
        if e.errno == 48:  # Address already in use
            divine_log("Port 8765 is in use. Please clear the sacred channel first.", "warning")
            divine_log("Use: lsof -i :8765 to find the process", "info")
        else:
            divine_log(f"Sacred Error: {str(e)}", "error")
    except KeyboardInterrupt:
        divine_log("Sacred Shutdown Initiated...", "warning")
    except Exception as e:
        divine_log(f"Unexpected Sacred Event: {str(e)}", "error")

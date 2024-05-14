import threading
import time


def server_status():
    """Simulated function to print server status every 2 seconds"""
    while True:
        # This will print indefinitely until the main program exists
        print('[Server Status]: Running')
        time.sleep(2)


t = threading.Thread(target=server_status)

t.daemon = True  # If daemon = False, then there will be infinity loop

t.start()


def run_server():
    """Simulated function for server main loop"""
    for _ in range(10):
        # Simulate the server doing some work
        print("[Server]: Processing data...")
        time.sleep(1)


run_server()
print("Server shutdown.")

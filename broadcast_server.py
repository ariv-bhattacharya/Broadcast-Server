import socket
import threading
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MAX_CONNECTIONS = 5 # Maximum number of concurrent connections

class BroadcastServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock() # To protect the clients list from race conditions
        self.server_socket = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAX_CONNECTIONS)
            self.running = True
            print(f"Server listening on {self.host}:{self.port}")
            self.accept_connections()
        except OSError as e:
            print(f"Error starting server: {e}")
            self.shutdown()

    def accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0) # Timeout for accept to allow graceful shutdown
                conn, addr = self.server_socket.accept()
                self.server_socket.settimeout(None) # Reset timeout
                with self.lock:
                    self.clients.append(conn)
                print(f"Connected by {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True # Allow main program to exit even if threads are running
                client_thread.start()
            except socket.timeout:
                continue # Continue waiting for connections
            except OSError as e:
                if self.running: # Only print error if server is still supposed to be running
                    print(f"Error accepting connection: {e}")
                break # Break if server socket is closed

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                self.broadcast_message(message, sender_conn=conn)
        except OSError as e:
            print(f"Client {addr} error: {e}")
        finally:
            print(f"Client {addr} disconnected")
            with self.lock:
                if conn in self.clients:
                    self.clients.remove(conn)
            conn.close()

    def broadcast_message(self, message, sender_conn=None):
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_conn: # Don't send message back to the sender
                    try:
                        client_socket.sendall(f"[Broadcast] {message}".encode('utf-8'))
                    except OSError as e:
                        print(f"Error broadcasting to client: {e}")
                        # Optionally, you could try to remove the client here,
                        # but it's handled in handle_client when recv fails.

    def shutdown(self):
        print("Shutting down server...")
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        with self.lock:
            for client_socket in self.clients:
                try:
                    client_socket.sendall("Server is shutting down.".encode('utf-8'))
                    client_socket.close()
                except OSError as e:
                    print(f"Error closing client socket during shutdown: {e}")
            self.clients.clear()
        print("Server shut down.")

def main():
    server = BroadcastServer(HOST, PORT)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down server...")
    finally:
        server.shutdown()

if __name__ == "__main__":
    main()
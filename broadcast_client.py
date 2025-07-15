import socket
import threading
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class BroadcastClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.running = True
            print(f"Connected to server at {self.host}:{self.port}")

            # Start a thread to receive messages from the server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True # Allow main program to exit
            receive_thread.start()

            # Start sending messages from the main thread
            self.send_messages()
        except ConnectionRefusedError:
            print("Error: Connection refused. Is the server running?")
        except OSError as e:
            print(f"Error connecting to server: {e}")
        finally:
            self.shutdown()

    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    print("Server disconnected.")
                    self.running = False
                    break
                print(f"\n{data.decode('utf-8')}")
                sys.stdout.write("Enter message: ") # Prompt again after receiving
                sys.stdout.flush()
            except OSError as e:
                if self.running: # Only print error if client is still supposed to be running
                    print(f"Error receiving message: {e}")
                self.running = False
                break

    def send_messages(self):
        while self.running:
            try:
                message = input("Enter message: ")
                if message.lower() == 'exit':
                    break
                self.client_socket.sendall(message.encode('utf-8'))
            except OSError as e:
                print(f"Error sending message: {e}")
                self.running = False
                break
            except EOFError: # Handles Ctrl+D on some systems
                print("\nExiting client.")
                break
            except KeyboardInterrupt:
                print("\nExiting client.")
                break


    def shutdown(self):
        print("Shutting down client...")
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR) # Attempt to gracefully close both ends
                self.client_socket.close()
            except OSError as e:
                print(f"Error during client socket shutdown: {e}")
        print("Client shut down.")

def main():
    client = BroadcastClient(HOST, PORT)
    try:
        client.connect()
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down client...")
    finally:
        client.shutdown()

if __name__ == "__main__":
    main()
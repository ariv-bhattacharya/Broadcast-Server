"Simple Broadcast Chat Application"

This repository contains a basic client-server application that demonstrates a broadcast chat functionality using Python's socket and threading modules. The server listens for incoming client connections and broadcasts any received messages to all connected clients (excluding the sender).


Features--
1. Broadcast Messaging: Messages sent by one client are relayed to all other connected clients.
2. Multi-client Support: Handles multiple concurrent client connections using threading.
3. Graceful Shutdown: Includes mechanisms for both the server and clients to shut down cleanly.


Getting Started--

These instructions will help you set up a copy of the project on your local machine for development and testing purposes.


Prerequisites--

You need Python 3 installed on your system.


Installation--

Clone the repository:
git clone https://github.com/your-username/your-repo-name.git 
cd your-repo-name
(Replace your-username and your-repo-name with your actual GitHub details.)

Ensure the files are in the same directory:
Make sure broadcast_server.py and broadcast_client.py are in the same directory.


Usage--
1. Start the Server
Open a terminal or command prompt and run the server script:
python broadcast_server.py

You should see output similar to:
Server listening on 127.0.0.1:65432

2. Start Clients
Open one or more new terminals or command prompts for each client you want to connect. Run the client script in each:
python broadcast_client.py

You should see output similar to:
Connected to server at 127.0.0.1:65432
Enter message:

3. Chat!
In any client terminal, type a message and press Enter.
-The message will be sent to the server, which will then broadcast it to all other connected clients.

Example Interaction:

Server Terminal:

Server listening on 127.0.0.1:65432
Connected by ('127.0.0.1', 50000)
Connected by ('127.0.0.1', 50001)
Received from ('127.0.0.1', 50000): Hello everyone!

Client 1 Terminal:

Connected to server at 127.0.0.1:65432
Enter message: Hello everyone!
[Broadcast] Hello everyone!
Enter message:

Client 2 Terminal:

Connected to server at 127.0.0.1:65432
Enter message: Hi Client 1!
[Broadcast] Hello everyone!
[Broadcast] Hi Client 1!
Enter message:

Shutting Down--
To shut down a client: Type exit and press Enter in the client's terminal, or press Ctrl+C.

To shut down the server: Press Ctrl+C in the server's terminal. The server will attempt to notify and disconnect all connected clients gracefully.

Project Structure---
1. broadcast_server.py: Contains the BroadcastServer class responsible for accepting connections, receiving messages, and broadcasting them.

2. broadcast_client.py: Contains the BroadcastClient class responsible for connecting to the server, sending messages, and receiving broadcast messages.

Configuration--
The HOST and PORT variables are defined at the top of both broadcast_server.py and broadcast_client.py.

HOST: Default is 127.0.0.1 (localhost). You can change this to your server's IP address if you want to run it across different machines on a network.

PORT: Default is 65432. Ensure this port is not in use by another application.

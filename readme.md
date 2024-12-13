# Subnet Calculator Server

This project implements a **Subnet Calculator Server** using Python. It consists of a server (`server.py`) that listens for client connections and allows users to calculate information about IPv4 and IPv6 subnets, such as the number of usable addresses, the first usable address, and the last usable address. A client (`client.py`) connects to the server and interacts with it via a simple text-based interface.

## Features
- **User Authentication:** Basic username and password authentication.
- **IPv4 and IPv6 Support:** Supports both IPv4 and IPv6 subnet calculations.
- **Subnet Details:** Provides the number of usable addresses, the first usable address, and the last usable address for a given subnet.
- **Interactive Client:** A client program allows users to interact with the server and perform subnet calculations.

## Prerequisites
- Python 3.6+
- The `ipcalc` library (for subnet calculations).

Install `ipcalc` via pip if not already installed:
```bash
pip install ipcalc
```

## Project Files
### 1. `server.py`
The server script implements the following functionalities:
- Handles multiple client connections.
- Authenticates users based on predefined credentials.
- Processes user input to calculate subnet information.

### 2. `client.py`
The client script connects to the server and provides an interface to:
- Log in using a username and password.
- Select IPv4 or IPv6 subnet calculations.
- Input subnets in CIDR notation (e.g., `192.168.1.0/24` or `2001:db8::/48`).

## How to Run
### 1. Start the Server
Run the server script to start the server on port `65432`:
```bash
python server.py
```
The server will display a message:
```
Servidor escutando na porta 65432...
```

### 2. Start the Client
Run the client script to connect to the server:
```bash
python client.py
```

Follow the prompts in the client terminal to log in and perform subnet calculations.

### Example Interaction
#### Client Terminal:
```
Login: admin
Password: password123
Authentication successful.
MENU
1: IPv4
2: IPv6
0: Sair

OPTION: 1
Input the subnet (ex: 192.168.1.10/24 or 2001:db8::/48): 192.168.1.0/24
Number of useful addresses: 254
First address: 192.168.1.1
Last address: 192.168.1.254
MENU
1: IPv4
2: IPv6
0: Sair

OPTION: 0
Closing connection.
```

## How It Works
### Authentication
The server uses a dictionary (`USERS`) for storing predefined usernames and passwords. If authentication fails, the connection is closed.

### Subnet Calculations
The server uses the `ipcalc` library to calculate:
- **Number of usable addresses:**
  - For IPv4: Total addresses minus 2 (network and broadcast).
  - For IPv6: All addresses are typically usable unless reserved.
- **First and last usable addresses:** Determined using `ipcalc` functions.

### Communication
The server and client communicate over TCP. The client sends inputs to the server, and the server processes them, sending results back to the client.

## Notes
- The server binds to all network interfaces (`0.0.0.0`) and listens on port `65432`. You can change the port in `server.py` if needed.
- The client connects to `127.0.0.1` (localhost). For remote connections, replace it with the server's IP address.
- Ensure the `ipcalc` library is installed on both the server and client systems.

## Future Improvements
- Add support for SSL/TLS to secure communication.
- Implement a database for storing user credentials instead of hardcoding them.
- Allow multiple concurrent clients using threading or asynchronous programming.
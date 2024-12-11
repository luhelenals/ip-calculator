import socket
import ipaddress

# Dados de autenticação
USERS = {"admin": "password123"}

def calculate_subnet_info(subnet):
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        num_usable_addresses = max(0, network.num_addresses - 2)  # Exclui endereço de rede e broadcast (IPv4)
        usable_hosts = list(network.hosts())
        
        first_usable = usable_hosts[0] if usable_hosts else "N/A"
        last_usable = usable_hosts[-1] if usable_hosts else "N/A"
        
        return {
            "num_usable_addresses": num_usable_addresses,
            "first_usable": str(first_usable),
            "last_usable": str(last_usable)
        }
    except ValueError as e:
        return {"error": str(e)}

def handle_client(client_socket):
    client_socket.send(b"Login: ")
    username = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Password: ")
    password = client_socket.recv(1024).decode().strip()
    
    if USERS.get(username) != password:
        client_socket.send(b"Authentication failed. Closing connection.\n")
        client_socket.close()
        return
    
    client_socket.send(b"Authentication successful.\n")
    
    while True:
        client_socket.send(b"Choose type (1: IPv4, 2: IPv6, 0: Exit): ")
        choice = client_socket.recv(1024).decode().strip()
        
        if choice == "0":
            client_socket.send(b"Goodbye!\n")
            client_socket.close()
            break
        elif choice not in ["1", "2"]:
            client_socket.send(b"Invalid choice.\n")
            continue

        client_socket.send(b"Enter subnet (e.g., 192.168.1.10/24 or 2001:db8::/48): ")
        subnet = client_socket.recv(1024).decode().strip()
        
        result = calculate_subnet_info(subnet)
        if "error" in result:
            client_socket.send(f"Error: {result['error']}\n".encode())
        else:
            response = (
                f"Usable Addresses: {result['num_usable_addresses']}\n"
                f"First Usable: {result['first_usable']}\n"
                f"Last Usable: {result['last_usable']}\n"
            )
            client_socket.send(response.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 65432))
    server.listen(5)
    print("Server listening on port 65432...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
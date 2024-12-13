import socket
import ipcalc

# Dados de autenticação
USERS = {"admin": "password123"}

def calculate_subnet_info(subnet, choice):
    try:
        network = ipcalc.Network(subnet)
        num_usable_addresses = network.size() - 2 if choice == '1' else network.size() # Exclui endereço de rede e broadcast (IPv4)
        
        first_usable = network.host_first()
        last_usable = network.host_last()
        
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
        client_socket.send(b"MENU\n1: IPv4\n2: IPv6\n0: Exit\n\nOPTION: ")
        choice = client_socket.recv(1024).decode().strip()
        
        if choice == "0":
            client_socket.send(b"Closing connection.\n")
            client_socket.close()
            break
        elif choice not in ["1", "2"]:
            client_socket.send(b"Invalid option.\n")
            continue

        client_socket.send(b"Input the subnet (ex: 192.168.1.10/24 or 2001:db8::/48): ")
        subnet = client_socket.recv(1024).decode().strip()
        
        result = calculate_subnet_info(subnet, choice)
        if "error" in result:
            client_socket.send(f"Erro: {result['error']}\n".encode())
        else:
            response = (
                f"Number of useful addresses: {result['num_usable_addresses']}\n"
                f"First address: {result['first_usable']}\n"
                f"Last address: {result['last_usable']}\n"
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
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 65432))
    
    while True:
        response = client.recv(1024).decode()
        print(response, end="")
        if "Goodbye!" in response or "Authentication failed" in response:
            break
        data = input()
        client.send(data.encode())

    client.close()

if __name__ == "__main__":
    main()
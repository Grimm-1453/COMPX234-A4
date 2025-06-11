import socket
import sys
import threading

def handle_client(file_path, client_addr, main_sock):
    print(f"Handling request for {file_path} from {client_addr}")


def main():
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Server started on port {port}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received: {data.decode()} from {addr}")
        if msg[0] == "DOWNLOAD":
          file_path = os.path.join("files/server", msg[1])
          threading.Thread(
            target=handle_client,
            args=(file_path, addr, main_sock)
          ).start()

if __name__ == "__main__":
    main()
import socket
import sys

def main():
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Server started on port {port}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received: {data.decode()} from {addr}")

if __name__ == "__main__":
    main()
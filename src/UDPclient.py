import socket
import sys

def main():
    host, port, file_list = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    with open(file_list) as f:
        for filename in f:
            sock.sendto(f"DOWNLOAD {filename.strip()}".encode(), (host, port))

if __name__ == "__main__":
    main()
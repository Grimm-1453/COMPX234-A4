import socket
import sys

def reliable_send(sock, msg, addr, max_retries=5):
    timeout = 1.0
    for attempt in range(max_retries):
        try:
            sock.sendto(msg.encode(), addr)
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            timeout *= 2
            print(f"Timeout (Attempt {attempt+1}), retrying...")
    return None
def main():
    host, port, file_list = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    with open(file_list) as f:
        for filename in f:
            sock.sendto(f"DOWNLOAD {filename.strip()}".encode(), (host, port))

if __name__ == "__main__":
    main()
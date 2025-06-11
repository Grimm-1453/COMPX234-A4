import socket
import threading
import os
import base64
import random
import sys
def handle_client(file_path, client_addr, main_sock):
    # 创建专用数据端口 (50000-51000)
    data_port = random.randint(50000, 51000)
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_sock.bind(('0.0.0.0', data_port))
    
    try:
        file_size = os.path.getsize(file_path)
        # 发送 OK 响应
        response = f"OK {os.path.basename(file_path)} SIZE {file_size} PORT {data_port}"
        main_sock.sendto(response.encode(), client_addr)
        
        with open(file_path, 'rb') as f:
            while True:
                data, addr = data_sock.recvfrom(1024)
                msg = data.decode().split()
                
                if msg[0] == "FILE" and msg[2] == "GET":
                    start = int(msg[4])
                    end = min(int(msg[6]), file_size-1)
                    f.seek(start)
                    chunk = f.read(end - start + 1)
                    b64_data = base64.b64encode(chunk).decode()
                    resp = f"FILE {msg[1]} OK START {start} END {end} DATA {b64_data}"
                    data_sock.sendto(resp.encode(), addr)
                
                elif msg[0] == "FILE" and msg[2] == "CLOSE":
                    data_sock.sendto(f"FILE {msg[1]} CLOSE_OK".encode(), addr)
                    break
                    
    finally:
        data_sock.close()

def main():
    port = int(sys.argv[1])
    main_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    main_sock.bind(('0.0.0.0', port))
    
    print(f"Server listening on port {port}")
    while True:
        data, addr = main_sock.recvfrom(1024)
        msg = data.decode().split()
        
        if msg[0] == "DOWNLOAD":
            file_path = os.path.join("files/server", msg[1])
            if os.path.exists(file_path):
                threading.Thread(
                    target=handle_client, 
                    args=(file_path, addr, main_sock)
                ).start()
            else:
                main_sock.sendto(f"ERR {msg[1]} NOT_FOUND".encode(), addr)

if __name__ == "__main__":
    main()
import socket
import sys
import base64
import time

def reliable_send(sock, msg, addr, max_retries=5):
    timeout = 1.0  # 初始超时 1 秒
    for attempt in range(max_retries):
        try:
            sock.sendto(msg.encode(), addr)
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            timeout *= 2  # 指数退避
            print(f"Timeout (Attempt {attempt+1}), retrying...")
    return None

def download_file(sock, server_addr, filename):
    # 请求下载
    resp = reliable_send(sock, f"DOWNLOAD {filename}", server_addr)
    if not resp or resp.startswith("ERR"):
        print(f"Download failed: {resp.split(' ')[1]}")
        return False
    
    # 解析响应
    parts = resp.split()
    file_size = int(parts[parts.index("SIZE")+1])
    data_port = int(parts[parts.index("PORT")+1])
    data_addr = (server_addr[0], data_port)
    
    # 创建本地文件
    with open(f"files/client/{filename}", 'wb') as f:
        downloaded = 0
        block_size = 1000
        
        while downloaded < file_size:
            start = downloaded
            end = min(downloaded + block_size - 1, file_size-1)
            
            # 请求数据块
            req = f"FILE {filename} GET START {start} END {end}"
            resp = reliable_send(sock, req, data_addr)
            
            if resp and "OK" in resp:
                # 提取并写入数据
                data_start = resp.index("DATA") + 5
                b64_data = resp[data_start:]
                binary_data = base64.b64decode(b64_data)
                f.seek(start)
                f.write(binary_data)
                
                downloaded += len(binary_data)
                print("*", end='', flush=True)  # 进度显示
        
        # 关闭连接
        reliable_send(sock, f"FILE {filename} CLOSE", data_addr)
        print(f"\nDownload complete: {filename}")
    return True

def main():
    host, port, file_list = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    with open(file_list) as f:
        for filename in f.readlines():
            download_file(sock, (host, port), filename.strip())

if __name__ == "__main__":
    main()
#storege_s

import socket
import threading
import os

storage_path = "nuvem"

def handle_client(conn):
    with conn:
        request = conn.recv(1024).decode()
        conn.send("OK".encode())
        if request.startswith("UPLOAD"):
            #file_path = os.path.join(storage_path, request.split()[1])
            nome = conn.recv(1024).decode()
            conn.send("OK".encode())
            file_content = conn.recv(1024)
            with open(nome, 'wb') as f:
                f.write(file_content)
            mover = "mv " + nome + " " + storage_path
            os.system(mover)
            conn.sendall(b'OK')
        elif request.startswith("DOWNLOAD"):
            file_path = os.path.join(storage_path, request.split()[1])
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    conn.sendall(f.read())
            else:
                conn.sendall(b'File not found')
        else:
            conn.sendall(b'Invalid command')

def main(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))
        s.listen()
        print(f"Storage server listening on port {port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])
    main(port)

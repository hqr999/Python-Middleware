#server1.py

import socket
import threading
import os

# EndereÃ§os dos servidores de armazenamento (host, port)
storage_servers = [
    ("localhost", 5001)
]

file_registry = {}
lock = threading.Lock()

def distribute_file(file_path, file_content):
    print("Arquivo " + file_path + " 1 Armazenado")
    server = storage_servers[len(file_registry) % len(storage_servers)]
    print("Arquivo " + file_path + " 2 Armazenado")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server)
        print("Arquivo " + file_path + " 3 Armazenado")
        s.send(b'UPLOAD')
        s.recv(1024).decode()
        s.send(file_path.encode())
        s.recv(1024).decode()
        s.sendall(file_content)
        response = s.recv(1024).decode()
        if response == "OK":
            with lock:
                file_registry[file_path] = server
            print("Upload bem sucedido")
            return f"File {file_path} stored in {server}"
        else:
            return f"Failed to store file {file_path}"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 5000))
        s.listen()
        print("Manager listening on port 5000")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    with conn:
        request = conn.recv(1024).decode()
        if request.startswith("UPLOAD"):
            conn.send("OK".encode())
            print(request)
            file_bytes = b""
            nome = conn.recv(1024).decode()
            conn.send("OK".encode())
            arq = conn.recv(1024)
            print(nome)
            file_bytes = arq
            print("<END>")
            #file = open(nome,"wb")
            #file.write(file_bytes)
            distribute_file(nome, file_bytes)
            #file.close()
            conn.send("Terminado".encode())
        elif request.startswith("DOWNLOAD"):
            conn.send("OK".encode())
            file_path = conn.recv(1024).decode()
            with lock:
               server = file_registry.get(file_path)
            if server:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(server)
                s.send(b'DOWNLOAD ')
                s.recv(1024).decode()
                s.sendall(file_path.encode())
                response = s.recv(1024)
                conn.sendall(response)
            else:
                conn.sendall(b'File not found')
        elif request == "LIST_FILES":
            with lock:
              files = "\n".join(file_registry.keys())
            conn.sendall(files.encode())
        else:
            conn.sendall(b'Invalid command')

if __name__ == '__main__':
    main()

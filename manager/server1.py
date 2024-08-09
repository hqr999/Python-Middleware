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

def distribute_file(file_path,tamanho):
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
        s.send(str(tamanho).encode())
        s.recv(1024).decode()
        #s.sendall(file_content)
        print(os.path.getsize(file_path)) #Já está errado aqui
        f = open(file_path,'rb')
        while (bloco := f.read(4096)):
            s.sendall(bloco)
        
        f.close()
        os.system("rm " + file_path)    
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
            nome = conn.recv(1024).decode()
            conn.send("OK".encode())
            tamanho = int(conn.recv(1024).decode())
            conn.send("OK".encode())
            f = open(nome,'wb')
            received = 0
            while received < tamanho:
                bloco = conn.recv(4096)
                if not bloco:
                    break
                f.write(bloco)
                received += len(bloco)
            print("received=",received," tamanho=",tamanho)
            print("<END>")
            distribute_file(nome,tamanho)
            f.close()
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

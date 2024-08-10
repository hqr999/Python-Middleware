#storege_s

import socket
import threading
import os

#Aqui coloque o caminho da pasta que você escolheu para colocar o arquivo, 
# o nome da pasta deve ser o mesmo que foi colocado na var mover. 
storage_path = "/home/henriqueqr/Documentos/Codigos/Python/Middleware/nuvem/"

def handle_client(conn):
    with conn:
        request = conn.recv(1024).decode()
        conn.send("OK".encode())
        if request.startswith("UPLOAD"):
            #file_path = os.path.join(storage_path, request.split()[1])
            nome = conn.recv(1024).decode()
            conn.send("OK".encode())
            tamanho = int(conn.recv(1024).decode())
            conn.send("OK".encode())
            #file_content = conn.recv(1024)
            f = open(nome,'wb')
            received = 0
            file_bytes = b''
            print(tamanho)
            while received < tamanho:
                bloco = conn.recv(4096)
                if not bloco:
                    break
                file_bytes += bloco
                received += len(bloco)
            f.write(file_bytes)
            #with open(nome, 'wb') as f:
             #   f.write(file_content)
            #mover = "mv " + nome +" nuvem"
            #os.system(mover)
            print("Estou aqui")
            f.close()
            conn.sendall(b'OK')
        elif request.startswith("DOWNLOAD"):
            nome = conn.recv(1024).decode()
            file_path = storage_path + nome
            if os.path.exists(file_path):
                f = open(file_path, 'rb')
                conn.send(str(os.path.getsize(file_path)).encode())
                conn.recv(1024).decode()
                while (bloco := f.read(4096)):
                    conn.sendall(bloco)
                #conn.sendall(f.read())
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

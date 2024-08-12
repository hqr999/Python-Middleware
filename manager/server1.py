#server1.py

import socket
import threading
import os

# EndereÃ§os dos servidores de armazenamento (host, port)
storage_servers = [
    ("localhost", 5001)
]

file_registry = {}   # Lista de Arquivos na Nuvem
lock = threading.Lock() # define acesso mutuamente exclusivo

# função para distribuir os arquivos pelos servers
def distribute_file(nome, tamanho):
    server = storage_servers[len(file_registry) % len(storage_servers)] # decide o server a armazenar o arquivo
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server)       # conecta com o server
        s.send(b'UPLOAD')       # envia a escolha
        s.recv(1024).decode()
        s.send(nome.encode())   # envia o nome
        s.recv(1024).decode()
        s.send(str(tamanho).encode()) # envia o tamanho
        s.recv(1024).decode()
        f = open(nome,'rb')            # abre o arquivo no modo leitura
        while (bloco := f.read(4096)): # envia o arquivo em blocos
            s.sendall(bloco)
        f.close()                      # fecha o arquivo
        os.system("rm " + nome)        # remove o arquivo do serve
        response = s.recv(1024).decode() # recebe se o foi concluido com sucesso ou não
        if response == "OK":             # se foi concluido com sucesso
            with lock:                   # diz que esta usando o recurso
                file_registry[nome] = server # registra o nome com o server que esta armazenado
            print("Upload bem sucedido")
            return f"Arquivo {nome} armazenado"
        else:
            return f"Failed to store file {nome}"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 5000))   # define IP, Porta
        s.listen()                    # mostra que esta escutando
        print("Manager listening on port 5000") 
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start() # manda a requisição ser execultada numa thread

# função para rodar requisições
def handle_client(conn):
    with conn:
        request = conn.recv(1024).decode()  # recebe a requisição
        if request.startswith("UPLOAD"):
            conn.send("OK".encode())
            nome = conn.recv(1024).decode() # recebe nome
            conn.send("OK".encode())   
            tamanho = int(conn.recv(1024).decode()) # recebe tamanho e convete para inteiro
            conn.send("OK".encode())
            f = open(nome,'wb')       # cria um arquivo no modo escrita
            received = 0
            file_bytes = b''          # armazena os bytes do arquivo recebido
            while received < tamanho: # recebe blocos de bytes do arquivo
                bloco = conn.recv(4096)
                if not bloco:
                    break
                file_bytes += bloco
                received += len(bloco)
            f.write(file_bytes)       # escreve os bytes do arquivo recebido
            distribute_file(nome,tamanho) # manda o arquivo para a nuvem
            f.close()                 # fecha o arquivo
            conn.send("Terminado".encode())
        elif request.startswith("DOWNLOAD"):
            conn.send("OK".encode())
            nome = conn.recv(1024).decode() # recebe o nome
            #conn.send("OK".encode())
            with lock:          # diz que esta usando o recurso
               server = file_registry.get(nome) # verifica qual server esta o arquivo
            if server:          # se existir o arquivo nos registros
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(server)     # conecta com o server que tem o arquivo
                s.send(b'DOWNLOAD ')  # envia o que ele quer fazer
                s.recv(1024).decode()
                s.sendall(nome.encode()) # envia o nome do arquivo
                tamanho = int(s.recv(1024).decode()) # recebe o tamanho do arquivo
                s.send(b'OK')
                f = open(nome,'wb')  # cria um arquivo com o nome no modo escrita
                received = 0
                file_bytes = b''     # armazena os bytes do arquivo recebido da nuvem
                while received < tamanho: # recebe o arquivo em blocos
                    bloco = s.recv(4096)
                    if not bloco:
                        break
                    file_bytes += bloco
                    received += len(bloco)
                f.write(file_bytes)    # escreve os bytes no arquivo
                f.close()              # fecha o arquivo
                print(received)
                conn.send(str(received).encode()) # envia o tamanho do arquivo para o cliente
                conn.recv(1024).decode()
                file = open(nome,'rb')    # abre p arquivo no modo leitura
                while (bloco := file.read(4096)): # envia o arquivo para o cliente em blocos
                    conn.sendall(bloco)
                file.close()              # fecha o arquivo
                os.system("rm " + nome)
            else:
                conn.sendall(b'File not found')
        elif request == "LIST_FILES":
            with lock:     
              files = "\n".join(file_registry.keys()) # faz uma lista com os arquivos no registro de upload
            conn.sendall(files.encode())              # envia a lista
        else:
            conn.sendall(b'Invalid command')

if __name__ == '__main__':
    main()
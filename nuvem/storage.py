#storege_s

import socket
import threading
import os

#Aqui coloque o caminho da pasta que você escolheu para colocar o arquivo, 
# o nome da pasta deve ser o mesmo que foi colocado na var mover. 
storage_path = "/home/henriqueqr/Documentos/Codigos/Python/Middleware/nuvem/"

# função que responde as requisições do manager
def handle_client(conn):
    with conn:
        request = conn.recv(1024).decode() # recebe o tipo de pedido
        conn.send("OK".encode())           # separa e confirma o recebimento
        if request.startswith("UPLOAD"):   # caso o pedido seja UPLOAD
            nome = conn.recv(1024).decode() # recebe o nome do arquivo
            conn.send("OK".encode())    
            tamanho = int(conn.recv(1024).decode()) # recebe o tamanho do arquivo
            nome = storage_path + nome
            conn.send("OK".encode()) 
            f = open(nome,'wb')             # abre o arquivo no modo escrita
            received = 0
            file_bytes = b''                # armazena os bytes do arquivo
            while received < tamanho:       # recebe o arquivo em blocos
                bloco = conn.recv(4096)
                if not bloco:
                    break
                file_bytes += bloco
                received += len(bloco)
            f.write(file_bytes)             # escreve os bytes no arquivo
            #mover = "mv " + nome +" nuvem" # define o caminho para mover o arquivo para a nuvem
            #os.system(mover)               # move o arquivo para a nuvem
            f.close()
            conn.sendall(b'OK')
        elif request.startswith("DOWNLOAD"): # caso o pedido seja DOWNLOAD
            nome = conn.recv(1024).decode()  # recebe o nome do arquivo que deseja fazer DOWNLOAD
            file_path = storage_path + nome  # faz um caminho com onde os arquivos estão armazenados + nome do arquivo
            if os.path.exists(file_path):    # verifica se o arquivo existe 
                file_size = os.path.getsize(file_path)
                conn.send(str(file_size).encode()) # manda o tamanho do arquivo
                conn.recv(1024).decode()
                f = open(file_path, 'rb')    # abre o arquivo em modo leitura 
                while (bloco := f.read(4096)): # envia o arquivo em blocos
                    conn.sendall(bloco)
                f.close()                   # fecha o arquivo
            else:   # caso o arquivo não exista
                conn.sendall(b'File not found')
        else:
            conn.sendall(b'Invalid command')

def main(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))    # define o par IP, Porta
        s.listen()                     # mostra que esta escutando
        print(f"Storage server listening on port {port}")
        while True:                    
            conn, addr = s.accept()    # conecta com o maneger
            threading.Thread(target=handle_client, args=(conn,)).start() # manda o pedido para uma treat possibilitando fazer mas conecções se nescessario

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])  # recebe o numero usado para a porta
    main(port)

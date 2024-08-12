#storege_s

import socket
import threading
import os

#Aqui coloque o caminho da pasta que você escolheu para colocar o arquivo, 
# o nome da pasta deve ser o mesmo que foi colocado na var mover. 
storage_path = os.path.dirname(os.path.abspath(__file__)) + "/" 

# EndereÃ§os dos servidores de armazenamento (host, port)
storage_servers = [
    ("localhost", 5001),
    ("localhost", 5002),
    ("localhost", 5003),
    ("localhost", 5004)
]

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
            posicaoServer = int(conn.recv(1024).decode()) # recebe o posicao do outro server
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
            f.close()
	    
            server = storage_servers[posicaoServer]
	    # Envia uma copia para outro server
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect(server)        # conecta com o server2
            s2.send(b'COPIA')       # envia a escolha
            s2.recv(1024).decode()
            nomecopia = os.path.basename(nome)
            s2.send(nomecopia.encode())    # envia o nome
            s2.recv(1024).decode()
            s2.send(str(tamanho).encode()) # envia o tamanho
            s2.recv(1024).decode()
    
            f = open(nome,'rb')            # abre o arquivo no modo leitura
            while (bloco := f.read(4096)): # envia o arquivo em blocos
                s2.sendall(bloco)
            f.close()                      # fecha o arquivo
            
            res2 = s2.recv(1024).decode()
            
            if(res2 == "OK"):
                conn.sendall(b'OK')
            else:
            	conn.sendall(b'NOT')
            
        elif request.startswith("COPIA"):   # caso o pedido seja UPLOAD2
            nome = conn.recv(1024).decode()   # recebe o nome do arquivo
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

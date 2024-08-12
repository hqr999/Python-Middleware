import socket
import os
manager_address = ("localhost", 5000)

    # função para upload de arquivos
def upload_file(file_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(manager_address)             # faz a conecção com o maneger
    s.send(b'UPLOAD')                      # manda o comando do que deseja fazer
    s.recv(1024).decode()                  # mostra que recebeu e separa os envios
    nome = os.path.basename(file_path)     # pega o nome do arquivo do caminho fornecido
    s.send(nome.encode())                  # envia o nome
    s.recv(1024).decode()                  # mostra que recebeu e separa os envios
    file_size = os.path.getsize(file_path) # pega o tamanho do arquivo
    s.send(str(file_size).encode())        # envia o tamanho
    s.recv(1024).decode()                  # mostra que recebeu e separa os envios
    f = open(file_path,'rb')               # abre o arquivo no modo leitura
    while (bloco := f.read(4096)):         # envia o arquivo em blocos de tamanho 4096 bits
        s.sendall(bloco)
    response = s.recv(1024).decode()       # confirma o recebimento
    print(response)

    # função responsavel por mostrar os arquivos na nuvem
def list_files():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(manager_address)          
    s.sendall(b'LIST_FILES')            # manda o comando do que deseja fazer
    response = s.recv(1024).decode()    # recebe um lista contendo os arquivos que estão na Nuvem
    print("Arquivos na Nuvem:")         
    print(response)                     # mostra a lista de Arquivos na Nuvem

    # função responsavel por baixar um arquivo da nuvem
def download_file(filename, download_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(manager_address)
    s.send(b'DOWNLOAD ')
    s.recv(1024).decode()
    s.sendall(filename.encode())        # envia o nome do arquivo que deseja receber
    #s.revc(1024).decode()
    response = s.recv(1024).decode()    # recebe "File not found" se o arquivo não for encontrado e o tamanho do arquivo se ele for encontrado
    s.send("OK".encode())
    if response == "File not found":    # se o arquivo não for encontrado
        print("File not found")
    else:                               # se ele foi encontrado
        tamanho = int(response)         # transforma o str em inteiro
        f = open(download_path, 'wb')   # abre o arquivo em modo escrita
        received = 0
        file_bytes = b''                # armazena os bytes do arquivo
        while received < tamanho:       # recebe o arquivo em blocos de tamanho 4096 bits
            bloco = s.recv(4096)
            if not bloco:
                break
            file_bytes += bloco
            received += len(bloco)
        f.write(file_bytes)             # escreve os bytes no arquivo
        f.close()                       # fecha o arquivo
        print(f"File {filename} downloaded successfully to {download_path}")

def main():
    while True: # Mantem o cliente ativo até a opção 4 ser escolida
        print("\nOptions:")
        print("1. Faça Upload")
        print("2. Faça Download")
        print("3. Lista dos arquivos na nuvem")
        print("4. Sair")
        choice = input("Sua escolha: ")   # recebe um numero de 1-4 que mostra a escolha do cliente

        if choice == '1':  # Cliente escolhou a opção de Upload
            file_path = input("De o caminho para o arquivo que quer fazer upload: ")  # recebe o caminho do arquivo como por exemplo "/home/seuUsuario/arquivo.txt"
            if os.path.exists(file_path) == True:   # verifica se o arquivo existe
               upload_file(file_path)
            else:                                   # segunda chance para digitar corretamente
                file_path = input("De o caminho para o arquivo que quer fazer upload: ")
                upload_file(file_path)
        elif choice == '2': # Cliente escolhou a opção de Download
            filename = input("Qual arquivo deseja fazer download: ")        # recebe o nome do arquivo que deseja fazer download
            download_path = input("De o caminho e o nome para o arquivo: ") # recebe o caminho que deseja armazenar o arquivo com o nome que deseja dalo como por exemplo "/home/seuUsuario/Documentos/arq.txt"
            download_file(filename, download_path)
        elif choice == '3':  # Cliente escolhou a opção de lista na Nuvem
            list_files()
        elif choice == '4':  # Cliente escolhou a opção de  Sair
            print("Saindo...")
            break           # Encerra o cliente
        else:
            print("Escolha inválida. Tente de novo!")   # Erro mostrado se numero digitado está fora das escolhas

if __name__ == '__main__':
    main()

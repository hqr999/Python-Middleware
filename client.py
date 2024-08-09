import socket
import os
manager_address = ("localhost", 5000)

def upload_file(file_path):
    f = open(file_path, 'rb')
    file_content = f.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(manager_address[1])
    s.connect(manager_address)
    s.send(b'UPLOAD')
    s.recv(1024).decode()
    nome = os.path.basename(file_path)
    s.send(nome.encode())
    s.recv(1024).decode()
    s.sendall(file_content )
    print(manager_address[0])
    response = s.recv(1024).decode()
    print(response)

def list_files():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(manager_address)
    s.sendall(b'LIST_FILES')
    response = s.recv(1024).decode()
    print("Files in the cloud:")
    print(response)

def download_file(filename, download_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(manager_address)
    s.send(b'DOWNLOAD ')
    s.recv(1024).decode()
    s.sendall(filename.encode())
    response = s.recv(1024)
    if response == b'File not found':
        print("File not found")
    else:
        f = open(download_path, 'wb')
        f.write(response)
        print(f"File {filename} downloaded successfully to {download_path}")

def main():
    while True:
        print("\nOptions:")
        print("1. Faça Upload")
        print("2. Faça Download")
        print("3. Lista dos arquivos na nuvem")
        print("4. Sair")
        choice = input("Sua escolha: ")

        if choice == '1':
            file_path = input("De o caminho para o arquivo que quer fazer upload: ")
            if os.path.exists(file_path) == True:
               upload_file(file_path)
            else:
                file_path = input("De o caminho para o arquivo que quer fazer upload: ")
        elif choice == '2':
            filename = input("Qual arquivo deseja fazer download: ")
            download_path = input("De o caminho e o nome para o arquivo: ")
            download_file(filename, download_path)
        elif choice == '3':
            list_files()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Escolha inválida. Tente de novo!")

if __name__ == '__main__':
    main()

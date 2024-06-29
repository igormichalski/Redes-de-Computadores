import socket
import sys
import subprocess
import threading

def enviar_string(ip, port, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        envia.connect((ip, port))
        print(f"Enviando mensagem para {ip}:{port}")

        # Enviar o tamanho da mensagem primeiro
        mensagem_bytes = mensagem.encode('utf-8')
        envia.send(len(mensagem_bytes).to_bytes(4, 'big'))
        envia.send(mensagem_bytes)

        print(f"Mensagem enviada com sucesso para {ip}:{port}")


def receber_arquivos(client_socket):
    try:
        # Receber o nome do arquivo
        file_name_size = client_socket.recv(4)
        if not file_name_size:
            return None
        file_name_size = int.from_bytes(file_name_size, 'big')
        file_name = client_socket.recv(file_name_size).decode('utf-8')

        # Receber o arquivo
        with open(file_name, 'wb') as arquivo:
            while True:
                ler_buffer = client_socket.recv(1024)
                if not ler_buffer:
                    break
                arquivo.write(ler_buffer)

        print(f"Arquivo {file_name} recebido com sucesso")
        return file_name

    except Exception as e:
        print(f"Ocorreu um erro ao receber o arquivo: {e}")
        return None

def compile_and_run(file):
    try:
        compile_cmd = f"gcc {file} -o {file.split('.')[0]}"
        result_compile = subprocess.run(compile_cmd, shell=True, check=True, capture_output=True)

        run_cmd = f"./{file.split('.')[0]}"
        result_run = subprocess.run(run_cmd, shell=True, check=True, capture_output=True)
        
        return result_run.stdout.decode()
        
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def handle_portal(portal_socket):
    try:
        file_name = receber_arquivos(portal_socket)
        if file_name:
            result = compile_and_run(file_name)
            print(f"Resultado da execução:\n{result}")
            
            # Enviar o resultado da execução de volta para o portal
            enviar_string('192.168.11.107', 8001, result) #ip de onde esta o portal

    except Exception as e:
        print(f"Erro no tratamento do portal: {e}")
    finally:
        portal_socket.close()

def main():
    if len(sys.argv) != 2:
        print("Uso: server.py <porta>")
        sys.exit(1)
    
    port = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('192.168.11.107', port)) #ip onde esta o servidor
        server_socket.listen(5)
        print(f"Servidor ouvindo em {server_socket.getsockname()}")

        while True:
            portal_socket, addr = server_socket.accept()
            print(f"Portal conectado de {addr}")
            portal_handler = threading.Thread(target=handle_portal, args=(portal_socket,))
            portal_handler.start()

if __name__ == "__main__":
    main()
import socket
import sys
import random

# Lista de servidores
servers = [("localhost", 9001), ("localhost", 9002), ("localhost", 9003)]

def enviar_string(ip, port, mensagem):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.connect((ip, port))
        print(f"Enviando mensagem para {ip}:{port}")

        # Enviar o tamanho da mensagem primeiro
        mensagem_bytes = mensagem.encode('utf-8')
        envia.send(len(mensagem_bytes).to_bytes(4, 'big'))
        envia.send(mensagem_bytes)

        print(f"Mensagem enviada com sucesso para {ip}:{port}")

def receber_resultado(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recebe:
        recebe.bind((ip, port))
        recebe.listen(1)
        resultado = ""
        
        conn, addr = recebe.accept()
        with conn:
            while True:
                dados = conn.recv(1024)
                if not dados:
                    break
                resultado += dados.decode('utf-8')

        return resultado

def enviar_arquivo(ip, port, nome_arquivo):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.connect((ip, port))
        nome_arquivo_bytes = nome_arquivo.encode('utf-8')
        envia.send(len(nome_arquivo_bytes).to_bytes(4, 'big'))
        envia.send(nome_arquivo_bytes)

        with open(nome_arquivo, "rb") as arquivo:
            ler_buffer = arquivo.read(1024)
            while ler_buffer:
                envia.send(ler_buffer)
                ler_buffer = arquivo.read(1024)

def receber_arquivos(client_socket):
    arquivos_recebidos = []
    try:
        while True:
            file_name_size = client_socket.recv(4)
            if not file_name_size:
                break
            file_name_size = int.from_bytes(file_name_size, 'big')
            file_name = client_socket.recv(file_name_size).decode('utf-8')

            with open(file_name, 'wb') as arquivo:
                while True:
                    ler_buffer = client_socket.recv(1024)
                    if not ler_buffer:
                        break
                    arquivo.write(ler_buffer)

            arquivos_recebidos.append(file_name)

    except Exception as e:
        print(f"Ocorreu um erro ao receber o arquivo: {e}")
    finally:
        return arquivos_recebidos

def handle_client(client_socket, mode, RR, addr):
    try:
        arquivos_recebidos = receber_arquivos(client_socket)

        resultado_final = ""

        if mode == "random":
            for arquivo in arquivos_recebidos:
                server = random.choice(servers)
                enviar_arquivo(server[0], server[1], arquivo)
                resultado = receber_resultado(server[0], 8001)
                resultado_final += resultado + "\n"

        elif mode == "round-robin":
            for arquivo in arquivos_recebidos:
                server = servers[RR]
                enviar_arquivo(server[0], server[1], arquivo)
                resultado = receber_resultado(server[0], 8001)
                resultado_final += resultado + "\n"
                RR = (RR + 1) % len(servers)

        print("Resultado do servidores: ")
        print(resultado_final)  

        # Enviar o resultado da execução de volta para o cliente
        enviar_string(addr[0], 8002, resultado_final)    

    except Exception as e:
        print(f"Erro no tratamento do cliente: {e}")
    finally:
        client_socket.close()
        return RR

def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ["0", "1"]:
        print("Uso: portal.py <porta> <modo>")
        print("  Modo: 0 para aleatório, 1 para round-robin.")
        sys.exit(1)

    port = int(sys.argv[1])
    mode = "round-robin" if sys.argv[2] == "1" else "random"
    RR = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"Portal ouvindo em {server_socket.getsockname()}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Cliente conectado de {addr}")
                RR = handle_client(client_socket, mode, RR, addr)
            except KeyboardInterrupt:
                print("\nEncerrando servidor...")
                break
            except Exception as e:
                print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()

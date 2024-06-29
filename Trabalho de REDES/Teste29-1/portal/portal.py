import socket
import sys
import random

# Lista de servidores
servers = [("192.168.11.137", 9001), ("192.168.11.137", 9002), ("192.168.11.137", 9003)] #Ips de onde estao os servidores, onde eles ficam ouvindo [IP_OndeServOuve]
IP_OndePortalOuve = ['192.168.11.137']
IP_PORTA_OndeClienteOuve = ['192.168.11.137', 8002] 


def enviar_string(ip, port, mensagem):
    #Retransmite a string "Resultado que obtivemos do Servidor finalizando: Portal >> Cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        envia.connect((ip, port))

        #Enviar o tamanho da mensagem primeiro e depois a mensagem
        mensagem_bytes = mensagem.encode('utf-8')
        envia.send(len(mensagem_bytes).to_bytes(4, 'big'))
        envia.send(mensagem_bytes)

def receber_resultado(ip, port):
    #Serve para receber a string "Resultado" que esta sendo trasmitida do Servidor >> Portal
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recebe:
        recebe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recebe.bind((IP_OndePortalOuve[0], port)) #|PORTA 8001| 
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
    #Inicia a conexao com o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        envia.connect((ip, port))

        #Enviar o nome do arquivo primeiro
        nome_arquivo_bytes = nome_arquivo.encode('utf-8')
        envia.send(len(nome_arquivo_bytes).to_bytes(4, 'big'))
        envia.send(nome_arquivo_bytes)

        #Enviar o conteúdo do arquivo
        with open(nome_arquivo, "rb") as arquivo:
            ler_buffer = arquivo.read(1024)
            while ler_buffer:
                envia.send(ler_buffer)
                ler_buffer = arquivo.read(1024)

def receber_arquivos(client_socket):
    arquivos_recebidos = []
    try:
        while True:
            #Recebe tamanho e nome do arquivo
            file_name_size = client_socket.recv(4)
            if not file_name_size:
                break
            file_name_size = int.from_bytes(file_name_size, 'big')
            file_name = client_socket.recv(file_name_size).decode('utf-8')

            #Recebe o conteudo do arquivo
            with open(file_name, 'wb') as arquivo:
                while True:
                    ler_buffer = client_socket.recv(1024)
                    if not ler_buffer:
                        break
                    arquivo.write(ler_buffer)

            arquivos_recebidos.append(file_name)

    except Exception as e:
        exit(1)
    finally:
        return arquivos_recebidos

def tratarCliente(client_socket, mode, RR):
    #Assim que um cliente conectou iniciamos o tratamento dele
    try:
        #Recebe o arquivo enviado pelo cliente
        arquivos_recebidos = receber_arquivos(client_socket)

        resultado_final = ""

        #Caminhos para o tipo de escolha de processamento
        if mode == "random":
            for arquivo in arquivos_recebidos:
                server = random.choice(servers) #Separa o servidor destino
                enviar_arquivo(server[0], server[1], arquivo) #Envia o Arquivo para o Servidor
                resultado = receber_resultado(server[0], 8001) #Chama a função que irá tratar a resposta do servidor
                resultado_final += resultado + "\n" #Armazena a resposta

        elif mode == "round-robin":
            for arquivo in arquivos_recebidos:
                server = servers[RR] #Separa o servidor destino
                enviar_arquivo(server[0], server[1], arquivo) #Envia o Arquivo para o Servidor
                resultado = receber_resultado(server[0], 8001) #Chama a função que irá tratar a resposta do servidor
                resultado_final += resultado + "\n" #Armazena a resposta
                RR = (RR + 1) % len(servers) #Atualiza index do Round Robin

    except Exception as e:
        exit(1)
    finally:
        client_socket.close()
        #Enviar o resultado da execução de volta para o cliente
        enviar_string(IP_PORTA_OndeClienteOuve[0], IP_PORTA_OndeClienteOuve[1], resultado_final)
        return RR

def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ["0", "1"]:
        sys.exit(1)

    port = int(sys.argv[1])
    mode = "round-robin" if sys.argv[2] == "1" else "random"
    RR = 0

    #Incia socket e fica aguardando uma conexão de cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP_OndePortalOuve[0], port))
        server_socket.listen(5)

        while True:
            try:
                client_socket, addr = server_socket.accept()
                RR = tratarCliente(client_socket, mode, RR)
            except KeyboardInterrupt:
                break
            except Exception as e:
                exit(1)

if __name__ == "__main__":
    main()
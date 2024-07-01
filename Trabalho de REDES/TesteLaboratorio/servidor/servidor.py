import socket
import sys
import subprocess
import threading

IP_PORTA_OndePortalOuve = ['172.26.2.143', 8001] #Porta 8001 usada como padrão para retorno de resultados
IP_OndeServOuve = ['172.26.2.149'] #Precisa ser a mesma que o pc onde o servidor esta

def enviar_string(ip, port, mensagem):
    #Inicia o processo de volta do resultado Fazendo o caminho Servidor >> Portal
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
        envia.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        envia.connect((ip, port))

        #Enviar o tamanho da mensagem primeiro e depois a mensagem
        mensagem_bytes = mensagem.encode('utf-8')
        envia.send(len(mensagem_bytes).to_bytes(4, 'big'))
        envia.send(mensagem_bytes)

def receber_arquivos(client_socket):
    try:
        #Recebe tamanho e nome do arquivo
        file_name_size = client_socket.recv(4)
        if not file_name_size:
            return None
        file_name_size = int.from_bytes(file_name_size, 'big')
        file_name = client_socket.recv(file_name_size).decode('utf-8')

        #Recebe o conteudo do arquivo
        with open(file_name, 'wb') as arquivo:
            while True:
                ler_buffer = client_socket.recv(1024)
                if not ler_buffer:
                    break
                arquivo.write(ler_buffer)

        return file_name

    except Exception as e:
        return None

def Executar(file):
    try:
        #Realiza o processo para compilar e rodar o arquivo
        compile_cmd = f"gcc {file} -o {file.split('.')[0]}"
        result_compile = subprocess.run(compile_cmd, shell=True, check=True, capture_output=True) #Cria um sub Processo para compilar o .c

        run_cmd = f"./{file.split('.')[0]}"
        result_run = subprocess.run(run_cmd, shell=True, check=True, capture_output=True) #Cria um sub Processo para Rodar a aplicação .exe
        
        #Se deu tudo certo retorna o resultado
        return result_run.stdout.decode()
        
    except subprocess.CalledProcessError as e:
        #Em caso de erro retorna o erro
        return e.stderr.decode()

def tratarPortal(portal_socket):
    try:
        #Recebe o arquivo enviado pelo Portal
        file_name = receber_arquivos(portal_socket) 
        if file_name:
            #Executa o arquivo.c e armazena o resultado
            result = Executar(file_name)
            
            #Enviar o resultado da execução de volta para o portal
            enviar_string(IP_PORTA_OndePortalOuve[0], IP_PORTA_OndePortalOuve[1], result)

    except Exception as e:
        exit(1)
    finally:
        portal_socket.close()

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    
    port = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        #Incia socket e fica aguardando uma conexão do portal
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP_OndeServOuve[0], port))
        server_socket.listen(5)

        while True:
            portal_socket, addr = server_socket.accept()
            #Inicializa uma tread
            portal_handler = threading.Thread(target=tratarPortal, args=(portal_socket,))
            portal_handler.start()

if __name__ == "__main__":
    main()

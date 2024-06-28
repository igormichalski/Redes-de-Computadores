#!/usr/bin/env python3

import socket
import sys
import os
import struct
import time

def list_files():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    if not files:
        print("L 0")
    else:
        print("L")
        for file in files:
            print(f"[{file}]")

def enviar_arquivos(ip, port, arquivos):
    for nome_arquivo in arquivos:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envia:
            envia.connect((ip, port))  # IP e a porta usada no servidor
            print(f"Enviando {nome_arquivo}")

            # Enviar o nome do arquivo primeiro
            nome_arquivo_bytes = nome_arquivo.encode('utf-8')
            envia.send(len(nome_arquivo_bytes).to_bytes(4, 'big'))
            envia.send(nome_arquivo_bytes)

            # Enviar o conteúdo do arquivo
            with open(nome_arquivo, "rb") as arquivo:
                ler_buffer = arquivo.read(1024)  # começa a ler o arquivo e armazenar em um buffer
                while ler_buffer:
                    envia.send(ler_buffer)  # envia o conteúdo do buffer para o servidor
                    ler_buffer = arquivo.read(1024)  # armazena mais conteúdo do arquivo no buffer

            print(f"Arquivo {nome_arquivo} enviado com sucesso\n")

def receber_resultado(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recebe:
        #Ip para onde o portal esta enviando a resposta #configurar para ser o ip do cliente que esta enviando o arquivo
        recebe.bind(('192.168.11.137', port)) #ip do portal
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

def main():
    if len(sys.argv) != 3:
        print("Uso: client.py <ip/nome_maquina> <porta>") #ip e porta do portal
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    portaString = 8002

    while True:
        resultadoFim = ""
        command = input().strip()
        if command.startswith('L'):
            list_files()
        elif command.startswith('S'):
            try:
                if command[2] == '[' and command[-1] == ']':
                    files = command[3:-1].strip().split(', ')
                    NumeroTotalArquivos = len(files)
                    enviar_arquivos(ip, port, files)
                else:
                    print("Formato inválido para o comando 'S'. Use: S [file1, file2, ...]")
            except IndexError:
                print("Formato inválido para o comando 'S'. Use: S [file1, file2, ...]")
        for i in range(len(files)):
            print(portaString)
            resultadoFim += receber_resultado(portaString) #criar um contador para mudar de porta porta++ (no portal tb) 
            portaString += 1
        print(resultadoFim)


if __name__ == "__main__":
    main()

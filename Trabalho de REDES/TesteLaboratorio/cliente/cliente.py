#!/usr/bin/env python3

import socket
import sys
import os

IP_PORTA_OndeClienteOuve = ['172.26.2.139', 8002] #(proprio ip do pc onde esta o cliente)

def list_files():
    #Simplismente lista os arquivos presentes no diretorio
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


def receber_resultado():
    #Serve para receber a string "Resultado" que esta sendo retransmitida do Servidor >> Portal >> Cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recebe:
        recebe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recebe.bind((IP_PORTA_OndeClienteOuve[0], IP_PORTA_OndeClienteOuve[1]))
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
        print("Uso: client.py <ip/nome_maquina> <porta>") #ip de onde esta o portal Porta = (8000)
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])

    while True:
        command = input().strip()
        if command.startswith('L'):
            list_files()
        elif command.startswith('S'):
            try:
                if command[2] == '[' and command[-1] == ']':
                    files = command[3:-1].strip().split(', ')
                    enviar_arquivos(ip, port, files)
            except IndexError: 
                exit(1)
        
        if command.startswith('S'):
            #Recebe o Resultado dos arquivos enviados para execução
            resultadoFim = ""
            for i in range(len(files)):
                resultadoFim += receber_resultado() 
            print(resultadoFim)


if __name__ == "__main__":
    main()

Igor Roberto Michalski de Souza

<<Antes de rodar>>
Verifique as variaveis no inicio de cada arquivo e os ips e porta dentro do arquivo 
make estejam com seus valores correto conforme a indicação dos comentarios

Verifique também que o nome dos computadores no arquivo make estão corretos


Executar os 3 (cliente, portal e servidor)
make


Rodar os codigos individualmente
- python3 cliente.py <Ip do Portal> <Porta do Portal>
- python3 portal.py <Porta onde Portal Ouve> <1(round robin) ou 0 (random)>
- python3 servidor.py <Porta Servidor>

*Exemplo
- python3 cliente.py 192.168.2.150 8000
- python3 portal.py 192.168.2.150 1
- python3 servidor.py 9001


Obs:
Porta 8001 padrão para retorno do resultado do servidor > portal
Porta 8002 padrão para retorno do resultado do portal > cliente

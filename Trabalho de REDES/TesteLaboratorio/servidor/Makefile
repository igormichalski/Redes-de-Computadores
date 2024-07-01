# Nome do Makefile: Makefile

# Variáveis
SERVER_SCRIPT = servidor.py
PORT1 = 9001
PORT2 = 9002
PORT3 = 9003

# Regras
all: chmod start_servers

# Define permissões de execução no script do servidor
chmod:
	chmod +x $(SERVER_SCRIPT)

# Inicia os três servidores em terminais diferentes
start_servers:
	@gnome-terminal -- bash -c 'python3 $(SERVER_SCRIPT) $(PORT1); exec $$SHELL'
	@gnome-terminal -- bash -c 'python3 $(SERVER_SCRIPT) $(PORT2); exec $$SHELL'
	@gnome-terminal -- bash -c 'python3 $(SERVER_SCRIPT) $(PORT3); exec $$SHELL'

# Limpeza (opcional)
clean:
	@echo "Nada para limpar"

.PHONY: all chmod start_servers clean

# Nome do Makefile: Makefile

# Variáveis
SERVER_SCRIPT = servidor.py
PORT = 9001

# Regras
all: run

# Define permissões de execução no script do servidor
chmod:
	@chmod +x $(SERVER_SCRIPT)

# Inicia os três servidores em terminais diferentes
run: chmod
	@./$(SERVER_SCRIPT) $(PORT)
# Limpeza (opcional)
clean:
	@echo "Nada para limpar"

.PHONY: all chmod run clean

# Nome do Makefile: Makefile

# Variáveis
SCRIPT = cliente.py

# Regras
all: run

# Define permissões de execução no script
chmod:
	@chmod +x $(SCRIPT)

# Executa o script (@ faz executar silenciosamente)
run: chmod
	@./$(SCRIPT) 172.26.2.143 8000 

# Limpeza (opcional)
clean:
	@echo "Nada para limpar"

.PHONY: all chmod run clean

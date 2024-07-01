# Nome do Makefile: Makefile

# Variáveis
SCRIPT = portal.py

# Regras
all: run

# Define permissões de execução no script
chmod:
	@chmod +x $(SCRIPT)

# Executa o script (@ faz executar silenciosamente)
run: chmod
	@./$(SCRIPT) 8000 1

# Limpeza (opcional)
clean:
	@echo "Nada para limpar"

.PHONY: all chmod run clean

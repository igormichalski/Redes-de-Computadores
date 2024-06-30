# Nome do Makefile: Makefile

# Variáveis
PORTAL_SCRIPT = portal.py 

# Regras
all: run

# Define permissões de execução no script do portal
chmod:
	@chmod +x $(PORTAL_SCRIPT)

#Executa o script (@ faz executar silenciosamente)
run: chmod
	@./$(PORTAL_SCRIPT) 8000 1

# Limpeza (opcional)
clean:
	@echo "Nada para limpar"

.PHONY: all chmod run clean

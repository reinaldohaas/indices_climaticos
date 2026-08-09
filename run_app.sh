#!/usr/bin/env bash
# Script de inicialização do Explorador Interativo de Índices Climáticos

echo "======================================================="
echo "  Explorador Interativo de Índices Climáticos"
echo "  Servidor Web Local"
echo "======================================================="
echo ""

# Find Python 3
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "ERRO: Python não encontrado no sistema. Por favor instale o Python 3."
    exit 1
fi

echo "Iniciando o servidor web na porta 8080 com $PYTHON_CMD..."
echo "Pressione Ctrl+C para encerrar o servidor."
echo ""

$PYTHON_CMD serve_app.py

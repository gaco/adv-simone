#!/bin/bash

echo "=================================================="
echo "   PORTFÓLIO Simone Persin Côrtes - ADVOCACIA"
echo "=================================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
    echo
fi

# Activate virtual environment
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/requirements_installed" ]; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
    touch venv/requirements_installed
    echo "✅ Dependências instaladas!"
    echo
fi

echo "Iniciando servidor Flask..."
echo
echo "URLs disponíveis:"
echo "  • Portfólio:        http://localhost:3000"
echo "  • Painel Admin:     http://localhost:3000/admin"
echo
echo "Pressione Ctrl+C para parar o servidor"
echo "=================================================="
echo

# Start the Flask application
python3 app.py 
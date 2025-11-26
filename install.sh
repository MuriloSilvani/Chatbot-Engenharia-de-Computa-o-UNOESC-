#!/bin/bash

echo "⚙️ Install Geral..."

echo "⚙️ [1/4] Verificando Python..."

if ! command -v python3 &> /dev/null
then
    echo "Python3 não encontrado! Instale com:"
    echo "brew install python"
    exit 1
fi

echo "⚙️ [2/4] Instalando dependências do backend..."
cd backend
sh install.sh

echo "⚙️ [3/4] Instalando dependências do frontend..."
cd ../frontend
sh install.sh

echo "⚙️ [4/4] Instalação completa!"
echo ""
echo "🔥 Para iniciar o projeto:"
echo "sh start.sh"
echo ""
echo "Chatbot configurado com sucesso! 🤖"

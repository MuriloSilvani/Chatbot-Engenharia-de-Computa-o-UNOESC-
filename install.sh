#!/bin/bash

echo "⚙️ Install Geral..."

echo "⚙️ [1/5] Verificando Python..."

if ! command -v python3 &> /dev/null
then
    echo "Python3 não encontrado! Instale com:"
    echo "brew install python"
    exit 1
fi

echo "⚙️ [2/5] Instalando dependências do scraper..."
cd scraper
sh install.sh

echo "⚙️ [3/5] Instalando dependências do backend..."
cd ../backend
sh install.sh

echo "⚙️ [4/5] Instalando dependências do frontend..."
cd ../frontend
sh install.sh

echo "⚙️ [5/5] Instalação completa!"
echo ""
echo "🔥 Para iniciar o projeto:"
echo "sh start.sh"
echo ""
echo "Chatbot configurado com sucesso! 🤖"

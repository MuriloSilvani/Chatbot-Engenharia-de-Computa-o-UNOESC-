#!/bin/bash

echo "⚙️ Install BACKEND..."

echo "[1/5] Verificando Python..."

if ! command -v python3 &> /dev/null
then
    echo "Python3 não encontrado! Instale com:"
    echo "brew install python"
    exit 1
fi

echo "Python3 encontrado: $(python3 --version)"

echo "[2/5] Criando ambiente virtual..."
python3 -m venv venv

echo "[3/5] Ativando ambiente..."
source venv/bin/activate

echo "[4/5] Instalando dependências..."
pip install -r requirements.txt

echo "[5/5] Instalação completa!"
echo ""
echo "🔥 Para iniciar o BACKEND:"
echo "sh start.sh"
echo ""

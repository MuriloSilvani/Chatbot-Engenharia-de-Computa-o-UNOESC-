#!/bin/bash

echo "========================================="
echo "     Rodando Aplicação Completa          "
echo "========================================="

BASE_FILE="./backend/ai/base_conhecimento.md"

if [ ! -f "$BASE_FILE" ]; then
    echo "📄 Base de conhecimento NÃO encontrada!"
    echo "▶️ Executando scraper..."
    ( cd scraper && bash start.sh )
    echo "✔ Scraper finalizado!"
else
    echo "📄 Base de conhecimento já existe. Pulando scraper."
fi

( cd backend && bash start.sh ) &
BACK_PID=$!

( cd frontend && bash start.sh ) &
FRONT_PID=$!

wait $BACK_PID
wait $FRONT_PID

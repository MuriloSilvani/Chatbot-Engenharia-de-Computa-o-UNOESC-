#!/bin/bash

echo "========================================="
echo "     Rodando Aplicação Completa          "
echo "========================================="

( cd backend && bash start.sh ) &
BACK_PID=$!

( cd frontend && bash start.sh ) &
FRONT_PID=$!

wait $BACK_PID
wait $FRONT_PID

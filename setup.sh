#!/bin/bash
set -e

echo "=================================================="
echo " Starting CTFd Platform + CTF Level Services"
echo "=================================================="

echo "[+] Building and starting containers..."
docker compose up -d --build

echo "[+] Waiting for Ollama container to initialize..."
until docker compose exec ollama ollama list > /dev/null 2>&1; do
    echo "    Waiting for Ollama service..."
    sleep 2
done

echo "[+] Pulling qwen2.5:0.5b model into Ollama..."
docker compose exec ollama ollama pull qwen2.5:0.5b

echo ""
echo "=================================================="
echo " ALL SERVICES READY & ROUTED TO SINGLE PORT (80)"
echo "=================================================="
echo " CTFd Main Platform:  http://localhost/"
echo " Web Level:           http://localhost/web-lvl/"
echo " AI Level:            http://localhost/ai-lvl/"
echo " Custom System Web:   http://localhost/custom/"
echo " Custom System Netcat: nc localhost 31337"
echo "=================================================="
echo " For Free Ngrok Plan (Single Port 80 Tunnel):"
echo "   ngrok http 80"
echo "=================================================="

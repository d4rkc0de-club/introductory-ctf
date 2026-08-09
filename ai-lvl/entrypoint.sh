ollama serve &

echo "Waiting for Ollama to start..."
while ! curl -s http://127.0.0 > /dev/null; do
    sleep 1
done

echo "Pulling AI model..."
ollama pull qwen2.5:0.5b

echo "Starting Flask server..."
exec gunicorn --bind 0.0.0.0:5021 app:app

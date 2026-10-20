# Benchmark script for evaluating performance of different local models pulled via ollama
# Benchmarking mistral 7b vs llamaa3.1 8b

import ollama

# Instantiate client explicitly pointing to host Ollama
client = ollama.Client(host="http://host.docker.internal:11434")

response = client.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Hello from Docker!"}],
)

print(response["message"]["content"])
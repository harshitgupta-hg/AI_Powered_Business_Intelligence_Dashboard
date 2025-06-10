import subprocess
import json

def ask_ollama(prompt):
    command = ['ollama', 'run', 'llama3']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

# Example usage
user_prompt = "Convert this to SQL: What is the total revenue last month?"
response = ask_ollama(user_prompt)
print(response)

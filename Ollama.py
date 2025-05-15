import subprocess
import requests
import json

class Ollama:
    def __init__(self,model='qwen2.5:7b'):
        self.model = model

    def query(self,prompt):
        command = ["ollama", "run", self.model, prompt]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print("Error during subprocess call:", e.stderr)
            return None
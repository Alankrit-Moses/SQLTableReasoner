import subprocess

class Ollama:
    def __init__(self, model='qwen2.5:7b'):
        self.model = model

    def query(self, prompt):
        command = ["ollama", "run", self.model]
        try:
            result = subprocess.run(
                command,
                input=prompt,               # send prompt via stdin
                text=True,                  # auto encode/decode as text
                capture_output=True,        # capture stdout and stderr
                check=True                  # raise exception if return code != 0
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print("Error during subprocess call:", e.stderr.strip())
            return None

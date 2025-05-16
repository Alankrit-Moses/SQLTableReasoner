import subprocess

class Ollama:
    def __init__(self, model='qwen3:4b', temperature=0.0, top_p=1.0):
        self.model = model
        self.temperature=str(temperature)
        self.top_p=str(top_p)

    def query(self, prompt):
        command = ["ollama", "run", "--temperature", self.temperature, "--top-p", self.top_p, self.model]
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

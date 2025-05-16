import requests, json

class Ollama:
    def __init__(self, model='qwen3:4b', host='http://localhost:11434'):
        self.model = model
        self.url   = f"{host}/api/generate"
        # default to fully-deterministic settings
        self.default_opts = {"temperature": 0, "top_p": 1, "seed": 42}

    def query(self, prompt: str, **extra_opts) -> str | None:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **{**self.default_opts, **extra_opts}
        }
        try:
            r = requests.post(self.url, json=payload, timeout=300)
            r.raise_for_status()
            return r.json()["response"].strip()
        except (requests.RequestException, KeyError) as e:
            print("Ollama API error →", e)
            return None

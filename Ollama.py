import requests, json

class Ollama:
    def __init__(self, model='qwen3:4b', host='http://localhost:11434'):
        self.model  = model
        self.url    = f'{host}/api/generate'        # use /api/chat for chat-style
        # deterministic defaults
        self.base_opts = {
            "temperature": 0,
            "top_p": 1,
            "seed": 42,         # reproducible
        }

    def query(self, prompt: str, max_tokens: int = 500, **extra_opts) -> str | None:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                **self.base_opts,
                "num_predict": max_tokens,   # ← max tokens
                **extra_opts                 # allow caller overrides
            }
        }
        try:
            r = requests.post(self.url, json=payload, timeout=300)
            r.raise_for_status()
            return r.json()["response"].strip()
        except (requests.RequestException, KeyError) as e:
            print("Ollama API error →", e)
            return None

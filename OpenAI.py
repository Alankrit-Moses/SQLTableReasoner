from openai import OpenAI

class OpenAIClient:
    def __init__OpenAIClient(self,model='gpt-4.1-mini', API_KEY = ''):
        self.client = OpenAI(api_key=API_KEY)
        self.model = model
    
    def set_model(self, model):
        self.model = model

    def get_response(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )
        return response
    
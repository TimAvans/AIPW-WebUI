import os
import yaml
import requests

class UniversalLLMController:
    def __init__(self, provider: str, config_path: str = "llm_config.yaml"):
        self.provider = provider.lower()
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)[self.provider]

        self.model = self.config.get("model")
        self.api_key = os.getenv(self.config.get("api_key_env"))
        self.endpoint = self.config.get("endpoint")
        self.headers = self.config.get("headers", {})
        self.body_template = self.config.get("body_template", {})
        self.response_path = self.config.get("response_path", [])

    def chat(self, messages, **kwargs):
        headers = self.headers.copy()

        if "$API_KEY" in self.endpoint:
            url = self.endpoint.replace("$API_KEY", self.api_key)
        elif "Authorization" in headers:
            headers["Authorization"] = headers["Authorization"].replace("$API_KEY", self.api_key)
            url = self.endpoint
        else:
            headers["Authorization"] = f"Bearer {self.api_key}"
            url = self.endpoint

        payload = {
            **self.body_template,
            "model": self.model,
            "messages": messages,
            **kwargs
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Traverse the response path
        for key in self.response_path:
            result = result[key]

        return result

# Usage example:
if __name__ == "__main__":
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    # {
    #     "role": msg["role"],
    #     "parts": [{"text": msg["content"]}]
    # }
    controller = UniversalLLMController(provider="gemini")
    print("Gemini:", controller.chat(messages))

    # controller = UniversalLLMController(provider="openai")
    # print("OpenAI:", controller.chat(messages))

    # controller = UniversalLLMController(provider="claude")
    # print("Claude:", controller.chat(messages))

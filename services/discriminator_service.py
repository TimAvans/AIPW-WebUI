import json
import os
from models.json_schema import discriminator_output

class Discriminator():
    """
    Evaluate the questionnaire data and return feedback for the generator
    """

    def __init__(self, openrouter_service, config_file="prompt.json", model=None, discriminator_prompt=None):
        self.openrouter_service = openrouter_service
        self.config_file = config_file
        self.prompt = discriminator_prompt or self.get_prompt()
        self.model = model or self.get_model()

    def discriminate(self, questionnaire_data, filepath):
        """
        Evaluate the questionnaire data and return feedback for the generator
        """
        prompt = f"{self.prompt} <questionnaire> {questionnaire_data} </questionnaire>"
        summary = self.openrouter_service.pdf_extraction_request_structured_output(message=prompt, model=self.model, pdf_path=filepath, response_format=discriminator_output)
        json_data = summary["choices"][0]["message"]["content"]
        json_data = json.loads(json_data)
        return json_data
    
    def get_prompt(self):
        """
        Get the prompt
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)
                return prompt_data["discriminator_prompt"]
        else:
            return self.prompt

    def get_model(self):
        """
        Get the model
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)
                return prompt_data["discriminator_model"]
        else:
            return self.model

import json
import os
from models.json_schema import generator_output
from services.csv_service import CSVService

class Generator():
    """
    Generate a questionnaire from a given prompt
    """

    def __init__(self, openrouter_service, config_file="prompt.json", model=None, generator_prompt=None):
        self.openrouter_service = openrouter_service
        self.config_file = config_file
        self.prompt = generator_prompt or self.get_prompt()
        self.model = model or self.get_model()
        self.csv_service = CSVService()
    
    def generate(self, filepath, feedback_prompt="<feedback>Deze sectie bevat normaal gesproken feedback op het vorige resultaat. </feedback>"):
        """
        Generate a questionnaire from a given prompt
        """
        summary = self.openrouter_service.pdf_extraction_request_structured_output(message=f"{self.prompt} {feedback_prompt}", model=self.model, pdf_path=filepath, response_format=generator_output)
        # print(summary)
        json_data = summary["choices"][0]["message"]["content"]
        json_data = json.loads(json_data)
        csv_string = self.csv_service.convert_questionnaire_json_to_csv(json_data=json_data)
        return csv_string

    def get_prompt(self):
        """
        Get the prompt
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)
                return prompt_data["generator_prompt"]
        else:
            return self.prompt

    def get_model(self):
        """
        Get the model
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)
                return prompt_data["generator_model"]
        else:
            return self.model

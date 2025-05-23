import requests
import json
from dotenv import load_dotenv
import os
import base64
from pathlib import Path
from models.json_schema import generator_output

class OpenRouterService():
    """Service for communicating with the OpenRouter API"""

    def __init__(self, api_key=None, url=None) -> None:
        load_dotenv()
        self.api_key = api_key or os.getenv('ROUTER_API_KEY')
        self.url = url or os.getenv('ROUTER_API_URL')

    def chat_request(self, message, model="openai/gpt-4o"):
        """Request for a regular chatrequest with the OpenRouter API"""
        response = requests.post(
        url=self.url,
        headers={
            "Authorization": f"Bearer {self.api_key}",
        },
        data=json.dumps({
            "model": model,
            "messages": [
            {
                "role": "user",
                "content": message
            }
            ]
        })
        )
        return response
    
    def encode_pdf_to_base64(self, pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')

    
    def pdf_extraction_request_structured_output(self, message, pdf_path, model="openai/gpt-4o", response_format=generator_output):
        """Request for extracting text from a PDF file and returning a structured output"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        content_blocks = [{
            "type": "text",
            "text": message
        }]

        # print(f"Processing pdf {pdf_path}")
        base64_pdf = self.encode_pdf_to_base64(pdf_path)
        data_url = f"data:application/pdf;base64,{base64_pdf}"
        filename = Path(pdf_path).name
        
        # print(f"Data url: {data_url}")

        content_blocks.append({
            "type": "file",
            "file": {
                "filename": filename,
                "file_data": data_url
            }
        })
        
        messages = [
            {
                "role": "user",
                "content": content_blocks
            }
        ]
       
        plugins = [
            {
                "id": "file-parser",
                "pdf": {
                    "engine": "pdf-text"  # defaults to "mistral-ocr"
                }
            }
        ]
        payload = {
            "model": model,
            "messages": messages,
            "plugins": plugins,
            "response_format": response_format
        }

        response = requests.post(self.url, headers=headers, json=payload)
        print(response.json())
        return response.json()

    def pdf_extraction_request(self, message, pdf_path, model="openai/gpt-4o"):
        """Request for extracting text from a PDF file"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        content_blocks = [{
            "type": "text",
            "text": message
        }]

        # for path in pdf_paths:
        # print(f"Processing pdf {pdf_path}")
        base64_pdf = self.encode_pdf_to_base64(pdf_path)
        data_url = f"data:application/pdf;base64,{base64_pdf}"
        filename = Path(pdf_path).name
        
        # print(f"Data url: {data_url}")

        content_blocks.append({
            "type": "file",
            "file": {
                "filename": filename,
                "file_data": data_url
            }
        })
        
        messages = [
            {
                "role": "user",
                "content": content_blocks
            }
        ]
       
        plugins = [
            {
                "id": "file-parser",
                "pdf": {
                    "engine": "pdf-text"  # defaults to "mistral-ocr"
                }
            }
        ]
        payload = {
            "model": model,
            "messages": messages,
            "plugins": plugins
        }

        response = requests.post(self.url, headers=headers, json=payload)
        print(response.json())
        return response.json()

if __name__ == "__main__":
    controller = OpenRouterService()
    message = "Hello, what can you do?"
    response = controller.chat_request(message)
    
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
        json_response = response.json()
        print(f'Message: {json_response["choices"][0]["message"]["content"]}')
    except json.JSONDecodeError:
        print("Response Text:", response.text)

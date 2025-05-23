from pydantic import BaseModel

class LLMConfig(BaseModel):
    generator_model: str
    generator_prompt: str
    generator_parameters: list[str] = []
    discriminator_model: str
    discriminator_prompt: str
    discriminator_parameters: list[str] = []
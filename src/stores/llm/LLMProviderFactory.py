from .LLMEnum import LLMEnums
from .providers import OpenAIProvider

class LLMProviderFactory:
    def __init__(self, config : dict):
        self.config = config


    def create(self, provider : str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url= self.config.OPENAI_API_URL,
                default_input_max_charachters = self.config.INPUT_DEFAULT_MAX_CHARACHTERS,
                default_generation_max_output_tokens= self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temprature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )


        return None
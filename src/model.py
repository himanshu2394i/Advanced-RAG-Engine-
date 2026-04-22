import logging
from abc import ABC, abstractmethod
import anthropic
import ollama

class BaseLLM(ABC):
    @abstractmethod
    def generate(self,messages_payload,system_prompt):
        pass

class AnthropicLLM(BaseLLM):
    def __init__(self,api_key,model_name="claude-3-haiku-20240307"):
        self.client= anthropic.Anthropic(api_key=api_key) if api_key else None
        self.model_name=model_name
    def generate(self,messages_payload, system_prompt,stream_to_console):
        if not self.client:
            raise ValueError("Anthropic API key is missing")
        message=self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            system=system_prompt,
            messages=messages_payload
        )
        result_text =message.content[0].text
        if stream_to_console:
            print(f"Bot: {result_text}\n")
        return result_text
    
class OllamaLLM(BaseLLM):
    def __init__(self,model_name="llama3.2"):
        self.model_name=model_name

    def generate(self,messages_payload,system_prompt,stream_to_console=True):
        ollama_messages=[{"role":"system","content":system_prompt}]+messages_payload
        stream_response= ollama.chat(model=self.model_name,messages=ollama_messages,stream=True)
        full_text= ""
        
        if stream_to_console:
            print("Bot : ",end="",flush=True)
        for chunk in stream_response:
            word= chunk['message']['content']
            print(word, end="", flush=True)
            full_text += word
        if stream_to_console:
            print()

        return full_text
    
class LLMRouter:
    def __init__(self,fallback_chain):
        self.fallback_chain=fallback_chain

    def run(self,messages_payload,system_prompt,stream_to_console=True):
        for model in self.fallback_chain:
            model_name=model.__class__.__name__
            logging.info(f"Attempting {model_name}")
            try:
                return model.generate(messages_payload,system_prompt,stream_to_console)
            except Exception as e:
                print(f"{model_name} failed: {e}.")
        return "Critical Error: All models in the fallback chain failed"


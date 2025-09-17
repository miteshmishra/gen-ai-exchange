import aiohttp
from typing import List, Dict, Any
from ..core.config import settings

class OllamaService:
    @staticmethod
    async def generate_completion(
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate completion using Ollama API
        """
        async with aiohttp.ClientSession() as session:
            url = f"{settings.OLLAMA_BASE_URL}/api/generate"
            
            # Format the messages similar to OpenAI's format
            prompt_text = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            payload = {
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt_text,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            try:
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error: {error_text}")
                    
                    result = await response.json()
                    return result.get("response", "")
            
            except Exception as e:
                print(f"Error calling Ollama API: {e}")
                raise
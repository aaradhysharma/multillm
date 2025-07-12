import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
import openai
import anthropic
import google.generativeai as genai
import cohere
import os
from config import LLMConfig, SYSTEM_PROMPT

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = os.getenv(config.api_key_env)
        if not self.api_key:
            raise ValueError(f"API key not found for {config.name}")
    
    @abstractmethod
    async def query(self, prompt: str) -> Tuple[str, str]:
        """Query the LLM and return (response, error_message)"""
        pass

class OpenAIClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = openai.AsyncOpenAI(api_key=self.api_key)
    
    async def query(self, prompt: str) -> Tuple[str, str]:
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            return response.choices[0].message.content, ""
        except Exception as e:
            return "", f"OpenAI Error: {str(e)}"

class AnthropicClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
    
    async def query(self, prompt: str) -> Tuple[str, str]:
        try:
            response = await self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text, ""
        except Exception as e:
            return "", f"Anthropic Error: {str(e)}"

class GoogleClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(config.model)
    
    async def query(self, prompt: str) -> Tuple[str, str]:
        try:
            # Google's API is not async, so we run in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.config.max_tokens,
                        temperature=self.config.temperature
                    )
                )
            )
            return response.text, ""
        except Exception as e:
            return "", f"Google Error: {str(e)}"

class CohereClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = cohere.AsyncClient(api_key=self.api_key)
    
    async def query(self, prompt: str) -> Tuple[str, str]:
        try:
            response = await self.client.chat(
                model=self.config.model,
                message=prompt,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                preamble=SYSTEM_PROMPT
            )
            return response.text, ""
        except Exception as e:
            return "", f"Cohere Error: {str(e)}"

class LLMClientFactory:
    """Factory for creating appropriate LLM clients"""
    
    @staticmethod
    def create_client(config: LLMConfig) -> LLMClient:
        """Create appropriate client based on config"""
        if "gpt" in config.model.lower() or "openai" in config.name.lower():
            return OpenAIClient(config)
        elif "claude" in config.model.lower() or "anthropic" in config.name.lower():
            return AnthropicClient(config)
        elif "gemini" in config.model.lower() or "google" in config.name.lower():
            return GoogleClient(config)
        elif "command" in config.model.lower() or "cohere" in config.name.lower():
            return CohereClient(config)
        else:
            # Default to OpenAI for unknown models
            return OpenAIClient(config)

class MultiLLMQueryEngine:
    """Main engine for querying multiple LLMs and evaluating responses"""
    
    def __init__(self):
        from config import Config
        self.config = Config
        self.enabled_llms = self.config.get_enabled_llms()
        self.judge_llm = self.config.get_judge_llm()
        
        if not self.enabled_llms:
            raise ValueError("No LLMs enabled or configured with API keys")
        
        if not self.judge_llm:
            raise ValueError("Judge LLM not configured")
    
    async def query_all_llms(self, prompt: str) -> Dict[str, Tuple[str, str]]:
        """Query all enabled LLMs concurrently"""
        tasks = []
        clients = []
        
        for llm_config in self.enabled_llms:
            try:
                client = LLMClientFactory.create_client(llm_config)
                clients.append((llm_config.name, client))
                tasks.append(client.query(prompt))
            except Exception as e:
                print(f"Failed to create client for {llm_config.name}: {e}")
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        responses = {}
        for (name, client), result in zip(clients, results):
            if isinstance(result, Exception):
                responses[name] = ("", f"Error: {str(result)}")
            else:
                responses[name] = result
        
        return responses
    
    async def evaluate_and_merge(self, prompt: str, responses: Dict[str, Tuple[str, str]]) -> str:
        """Use judge LLM to evaluate and merge responses"""
        # Format responses for evaluation
        response_text = ""
        for i, (name, (response, error)) in enumerate(responses.items(), 1):
            if error:
                response_text += f"\n{i}. {name}: ERROR - {error}\n"
            else:
                response_text += f"\n{i}. {name}:\n{response}\n"
        
        # Create evaluation prompt
        from config import EVALUATION_PROMPT
        evaluation_prompt = EVALUATION_PROMPT.format(
            query=prompt,
            responses=response_text
        )
        
        # Query judge LLM
        judge_client = LLMClientFactory.create_client(self.judge_llm)
        final_response, error = await judge_client.query(evaluation_prompt)
        
        if error:
            # Fallback: return best non-error response
            valid_responses = [(name, resp) for name, (resp, err) in responses.items() if not err and resp]
            if valid_responses:
                return f"Judge LLM failed ({error}). Best response from {valid_responses[0][0]}:\n\n{valid_responses[0][1]}"
            else:
                return f"All LLMs failed or Judge LLM error: {error}"
        
        return final_response
    
    async def process_query(self, prompt: str) -> Dict:
        """Main method to process a query through all LLMs and return merged result"""
        print(f"🔍 Querying {len(self.enabled_llms)} LLMs...")
        
        # Query all LLMs
        responses = await self.query_all_llms(prompt)
        
        print("📊 Evaluating and merging responses...")
        
        # Evaluate and merge
        final_response = await self.evaluate_and_merge(prompt, responses)
        
        return {
            "query": prompt,
            "individual_responses": responses,
            "final_response": final_response,
            "llms_used": [llm.name for llm in self.enabled_llms],
            "judge_llm": self.judge_llm.name
        } 
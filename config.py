import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, List, Optional

load_dotenv()

@dataclass
class LLMConfig:
    name: str
    api_key_env: str
    model: str
    max_tokens: int = 4000
    temperature: float = 0.7
    enabled: bool = True

class Config:
    # LLM Configurations
    LLMS: List[LLMConfig] = [
        LLMConfig(
            name="OpenAI GPT-4",
            api_key_env="OPENAI_API_KEY",
            model="gpt-4-turbo-preview",
            max_tokens=4000,
            temperature=0.7
        ),
        LLMConfig(
            name="Anthropic Claude",
            api_key_env="ANTHROPIC_API_KEY", 
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7
        ),
        LLMConfig(
            name="Google Gemini",
            api_key_env="GOOGLE_API_KEY",
            model="gemini-pro",
            max_tokens=4000,
            temperature=0.7
        ),
        LLMConfig(
            name="Cohere Command",
            api_key_env="COHERE_API_KEY",
            model="command-r-plus",
            max_tokens=4000,
            temperature=0.7
        ),
        LLMConfig(
            name="OpenAI GPT-3.5",
            api_key_env="OPENAI_API_KEY",
            model="gpt-3.5-turbo",
            max_tokens=4000,
            temperature=0.7
        ),
        LLMConfig(
            name="xAI Grok",
            api_key_env="GROK_API_KEY",
            model="grok-beta",
            max_tokens=4000,
            temperature=0.7
        )
    ]
    
    # Judge LLM (used for evaluation and merging)
    JUDGE_LLM = LLMConfig(
        name="OpenAI GPT-4 Judge",
        api_key_env="OPENAI_API_KEY",
        model="gpt-4-turbo-preview",
        max_tokens=4000,
        temperature=0.3  # Lower temperature for more consistent evaluation
    )
    
    @classmethod
    def get_enabled_llms(cls) -> List[LLMConfig]:
        """Get list of enabled LLMs that have API keys configured"""
        enabled = []
        for llm in cls.LLMS:
            if llm.enabled and os.getenv(llm.api_key_env):
                enabled.append(llm)
        return enabled
    
    @classmethod
    def get_judge_llm(cls) -> Optional[LLMConfig]:
        """Get judge LLM if API key is configured"""
        if os.getenv(cls.JUDGE_LLM.api_key_env):
            return cls.JUDGE_LLM
        return None

# Default prompt templates
EVALUATION_PROMPT = """
You are an expert AI evaluator. I will provide you with a user query and multiple responses from different AI models. Your job is to:

1. Analyze each response for accuracy, completeness, clarity, and helpfulness
2. Identify the best elements from each response
3. Create a comprehensive merged response that combines the best aspects
4. Provide reasoning for your choices

User Query: {query}

Responses:
{responses}

Please provide:
1. A brief evaluation of each response (2-3 sentences each)
2. A final merged response that incorporates the best elements
3. Your reasoning for the final response

Format your response as:
## Evaluation
[Your evaluation of each response]

## Final Response
[Your merged and improved response]

## Reasoning
[Your reasoning for the final response]
"""

SYSTEM_PROMPT = "You are a helpful, accurate, and comprehensive AI assistant. Provide detailed, well-structured responses that directly address the user's query." 
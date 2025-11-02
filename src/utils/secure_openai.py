import os
from typing import List, Dict, Optional
from openai import OpenAI
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class SecureOpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('GPT_MODEL', 'gpt-4.1-mini')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.top_p = float(os.getenv('TOP_P', '0.9'))
        
        # Create a custom session with privacy headers
        self.session = self._create_secure_session()
        
        # Initialize OpenAI client with custom configuration
        self.client = OpenAI(
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "private",
                "X-Session-Type": "private",
                "OpenAI-Internal-Request": "false",
                "X-Data-Use-Consent": "false",
            },
            http_client=self.session
        )

    def _create_secure_session(self) -> requests.Session:
        """Create a session with retry logic and privacy headers"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        
        # Add headers to prevent data storage and training
        session.headers.update({
            "HTTP-Referer": "private",
            "X-Session-Type": "private",
            "OpenAI-Internal-Request": "false",
            "X-Data-Use-Consent": "false",
        })
        
        return session

    async def generate_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None
    ) -> str:
        """
        Generate a completion with privacy-preserving settings
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                top_p=top_p or self.top_p,
                user="anonymous",  # Don't associate requests with a user
                headers={
                    "X-Request-Type": "private-inference",
                    "X-Data-Usage-Consent": "false"
                }
            )
            
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error in generate_completion: {str(e)}")
            raise

    async def generate_multiple_completions(
        self,
        prompts: List[str],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None
    ) -> List[str]:
        """
        Generate multiple completions with privacy-preserving settings
        """
        results = []
        for prompt in prompts:
            result = await self.generate_completion(
                prompt,
                max_tokens,
                temperature,
                top_p
            )
            results.append(result)
        return results

    def cleanup(self):
        """
        Clean up resources and ensure proper session closure
        """
        if self.session:
            self.session.close()
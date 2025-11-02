import os
from typing import List, Dict
from utils.secure_openai import SecureOpenAIClient

class LetterGenerator:
    def __init__(self):
        # Initialize secure OpenAI client
        self.ai_client = SecureOpenAIClient()
        
        # Load style examples and settings
        examples_path = os.getenv('LETTER_EXAMPLES_PATH', 'user_data/cover_letters/style_examples.md')
        with open(examples_path, 'r') as f:
            self.style_examples = f.read()
            
        self.tone = os.getenv('COVER_LETTER_TONE', 'professional')
        self.max_letters = int(os.getenv('MAX_COVER_LETTERS', '3'))
        
        # Output settings
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.save_intermediate = os.getenv('SAVE_INTERMEDIATE', 'false').lower() == 'true'
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    async def generate_letters(self, job_ad: str, num_variants: int = 3) -> List[Dict]:
        """Generate multiple versions of cover letters."""
        prompts = []
        
        for i in range(num_variants):
            prompt = f"""
            Create a cover letter for the following job posting.
            Use the style examples provided to maintain a natural, human-like tone.
            Each letter should be unique but maintain similar quality and professionalism.
            
            Style Examples:
            {self.style_examples}
            
            Job Advertisement:
            {job_ad}
            
            Generate version {i+1} of {num_variants}, with a different approach/focus for each version.
            """
            prompts.append(prompt)
        
        # Generate all letters in parallel for better performance
        responses = await self.ai_client.generate_multiple_completions(prompts)
        
        letters = [
            {
                'content': content,
                'version': i + 1
            }
            for i, content in enumerate(responses)
        ]
        
        return letters
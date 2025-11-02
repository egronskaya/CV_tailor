import os
import openai
from typing import List, Dict

class LetterGenerator:
    def __init__(self):
        # OpenAI settings
        self.model = os.getenv('GPT_MODEL', 'gpt-4.1-mini')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.top_p = float(os.getenv('TOP_P', '0.9'))
        openai.api_key = self.api_key
        
        # Load style examples and settings
        examples_path = os.getenv('LETTER_EXAMPLES_PATH', 'examples/cover_letters/style_examples.md')
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
    
    def generate_letters(self, job_ad: str, num_variants: int = 3) -> List[Dict]:
        """Generate multiple versions of cover letters."""
        letters = []
        
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
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            letter_content = response.choices[0].message.content
            
            letters.append({
                'content': letter_content,
                'version': i + 1
            })
        
        return letters
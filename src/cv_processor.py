import os
import openai
from typing import List, Dict

class CVProcessor:
    def __init__(self):
        # OpenAI settings
        self.model = os.getenv('GPT_MODEL', 'gpt-4.1-mini')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.top_p = float(os.getenv('TOP_P', '0.9'))
        openai.api_key = self.api_key
        
        # Load CV template and tailoring guide
        template_path = os.getenv('CV_TEMPLATE_PATH', 'templates/cv_template.tex')
        guide_path = os.getenv('CV_GUIDE_PATH', 'templates/cv_tailoring_guide.md')
        
        with open(template_path, 'r') as f:
            self.cv_template = f.read()
        
        with open(guide_path, 'r') as f:
            self.tailoring_guide = f.read()
            
        # Output settings
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.save_intermediate = os.getenv('SAVE_INTERMEDIATE', 'false').lower() == 'true'
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    def extract_skills(self, job_ad: str) -> List[str]:
        """Extract relevant skills from the job advertisement."""
        prompt = f"""
        Analyze the following job advertisement and extract a list of required skills,
        both technical and soft skills. Return them as a comma-separated list:
        
        {job_ad}
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        skills = response.choices[0].message.content.strip().split(',')
        return [skill.strip() for skill in skills]
    
    def tailor_cv(self, job_ad: str) -> Dict:
        """Generate a tailored CV based on the job advertisement."""
        prompt = f"""
        Use the following tailoring guide to customize a CV for this job posting.
        Return the CV content in a structured format that can be used with the LaTeX template.
        
        Tailoring Guide:
        {self.tailoring_guide}
        
        Job Advertisement:
        {job_ad}
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Process the response into a structured format
        # This would need to be adjusted based on the actual response format
        cv_content = response.choices[0].message.content
        
        # Return structured CV content
        return {
            'content': cv_content,
            'template': self.cv_template
        }
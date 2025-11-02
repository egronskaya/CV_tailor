import os
from typing import List, Dict
from utils.secure_openai import SecureOpenAIClient

class CVProcessor:
    def __init__(self):
        # Initialize secure OpenAI client
        self.ai_client = SecureOpenAIClient()
        
        # Load CV template and tailoring guide
        template_path = os.getenv('USER_CV_PATH', 'user_data/cv/user_cv.tex')
        guide_path = os.getenv('CV_GUIDE_PATH', 'user_data/templates/cv_tailoring_guide.md')
        
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
    
    async def extract_skills(self, job_ad: str) -> List[str]:
        """Extract relevant skills from the job advertisement."""
        prompt = f"""
        Analyze the following job advertisement and extract a list of required skills,
        both technical and soft skills. Return them as a comma-separated list:
        
        {job_ad}
        """
        
        response = await self.ai_client.generate_completion(prompt)
        skills = response.strip().split(',')
        return [skill.strip() for skill in skills]
    
    async def tailor_cv(self, job_ad: str) -> Dict:
        """Generate a tailored CV based on the job advertisement."""
        prompt = f"""
        Use the following tailoring guide to customize a CV for this job posting.
        Return the CV content in a structured format that can be used with the LaTeX template.
        
        Tailoring Guide:
        {self.tailoring_guide}
        
        Job Advertisement:
        {job_ad}
        """
        
        cv_content = await self.ai_client.generate_completion(prompt)
        
        # Return structured CV content
        return {
            'content': cv_content,
            'template': self.cv_template
        }
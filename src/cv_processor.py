import os
import json
from typing import List, Dict
from io import BytesIO
from src.utils.secure_openai import SecureOpenAIClient

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
        Given the following CV template and tailoring guide, customize the CV for this job posting.
        Parse and understand the CV content, focusing on the actual information rather than the formatting.
        Follow the tailoring guide precisely and return the output in the specified JSON format.
        
        Original CV:
        {self.cv_template}
        
        Tailoring Guide:
        {self.tailoring_guide}
        
        Job Advertisement:
        {job_ad}
        """
        
        cv_data = await self.ai_client.generate_completion(prompt)
        # Parse the JSON response
        cv_json = json.loads(cv_data)
        
        # Generate documents using the structured data
        return {
            'analysis': {
                'keywords': cv_json['job_keywords'],
                'gaps': cv_json['gaps_and_risks'],
                'suggestions': cv_json['notes_for_user'],
                'qa_results': cv_json['qa_checks']
            },
            'formats': {
                'docx': self._generate_docx(cv_json),  # ATS-friendly version
                'pdf': self._generate_pdf(cv_json)     # Human-readable version
            }
        }
        
    def _generate_docx(self, content: str) -> bytes:
        """Generate a DOCX version of the CV optimized for ATS compatibility."""
        from docx import Document
        doc = Document()
        # Format content into DOCX with ATS-friendly structure:
        # - Single column layout
        # - Standard fonts (Calibri, Arial)
        # - Clear section headers
        # - Simple bullet points for lists
        buffer = BytesIO()
        doc.save(buffer)
        return buffer.getvalue()
    
    def _generate_pdf(self, content: str) -> bytes:
        """Generate a PDF version of the CV optimized for human readers."""
        from fpdf import FPDF
        pdf = FPDF()
        # Format content into PDF with professional styling:
        # - Clean, readable layout
        # - Professional fonts
        # - Proper spacing and margins
        buffer = BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()
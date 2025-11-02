# CV Tailor

A Streamlit application that tailors CVs and cover letters to specific job advertisements using GPT-4. The application automatically adapts your CV and generates customized cover letters to maximize your chances of success with automated CV screening systems.

## Features

- Job advertisement analysis
- CV tailoring based on job requirements
- Generation of both PDF and DOCX formats
- Extraction of job-specific skills
- Generation of three unique cover letter variants
- Customizable CV and cover letter styling
- LaTeX-based CV templating

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your configuration:
   ```bash
   # Copy the example configuration
   cp .env.example .env
   
   # Edit the .env file with your settings
   nano .env
   ```

   Required environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GPT_MODEL`: The GPT model to use (default: gpt-4.1-mini)

   Optional configuration:
   - Model parameters (temperature, tokens, etc.)
   - Document generation settings
   - Output and formatting preferences
   - Debug and development options

   See `.env.example` for all available options and their descriptions.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Input the job advertisement text
3. The application will generate:
   - Tailored CV (PDF & DOCX)
   - Three versions of cover letters (PDF & DOCX)
   - List of job-specific skills

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── templates/
│   ├── cv_template.tex     # LaTeX CV template
│   └── style_guide.yaml    # Document styling configuration
├── src/
│   ├── cv_processor.py     # CV processing logic
│   ├── letter_generator.py # Cover letter generation
│   └── document_maker.py   # PDF/DOCX document creation
├── examples/
│   ├── cover_letters/      # Example cover letters for style matching
│   └── style_examples/     # CV styling examples
└── requirements.txt        # Project dependencies
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License